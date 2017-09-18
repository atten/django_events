import json

import requests
from django.contrib.postgres.fields import JSONField
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import translation, timezone
from django.utils.translation import ugettext_lazy as _
from furl import furl
from pytz import timezone as pytz_timezone

from events.models import Event
from events.serializers import LocalizedEventSerializer
from . import validators
from .mailer import DBMailerAPI, EmailSendError


class Destination(models.Model):
    app = models.CharField(max_length=100, unique=True)
    mailer_api_url = models.URLField(max_length=255)
    mailer_api_key = models.CharField(max_length=255)
    cas_profile_url = models.URLField(max_length=255,
                                      validators=[validators.validate_integer_placeholder],
                                      help_text="e.g. http://example.com/api/v1/profile/%d/. "
                                                "'%d' is required for substitute user_id.")
    cas_api_key = models.CharField(max_length=255)
    comment = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _('Destination')
        verbose_name_plural = _('Destinations')

    def __str__(self):
        return '%d: %s' % (self.id, self.comment or _('unnamed'))


class EventTriggerManager(models.QuerySet):
    def matches(self, event):
        for trigger in self.filter(app=event.app):
            q = Q(id=event.id) & Q(**trigger.lookup_kwargs)
            if Event.objects.filter(q).exists():
                yield trigger


class EventTrigger(models.Model):
    app = models.CharField(max_length=100)
    lookup_kwargs = JSONField()
    comment = models.CharField(max_length=255, blank=True, null=True)

    objects = EventTriggerManager.as_manager()

    class Meta:
        verbose_name = _('Event trigger')
        verbose_name_plural = _('Event triggers')

    def __str__(self):
        return '%d: %s' % (self.id, self.comment or _('unnamed'))


class EventReceiverPath(models.Model):
    path = models.CharField(max_length=128, unique=True,
                            help_text=_('Path to user_id in Event instance, e.g. "context.user.id"'))
    comment = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _('Event receiver path')
        verbose_name_plural = _('Event receiver paths')

    def extract_value(self, event):
        path = self.path.split('.')
        value = None
        for part in path:
            if value is None:
                value = getattr(event, part, None)
            elif isinstance(value, dict):
                value = value.get(part)
            else:
                return None
            if value is None:
                return None
        return value

    def __str__(self):
        ret = '%d: %s' % (self.id, self.path)
        if self.comment:
            ret += ' (%s)' % self.comment
        return ret


class NotifyTimeOptions(models.Model):
    """пока ничего не реализовано, кроме instant"""
    Kind_Instant = 0
    Kind_Delayed = 1
    Kind_Daily = 2
    Kind_Weekly = 7
    Kind_Monthly = 30

    KIND_CHOICES = (
        (Kind_Instant, 'instant'),
        (Kind_Delayed, 'delayed'),
        (Kind_Daily, 'daily'),
        (Kind_Weekly, 'weekly'),
        (Kind_Monthly, 'monthly'),
    )

    kind = models.SmallIntegerField(choices=KIND_CHOICES, default=Kind_Instant)
    time = models.TimeField(blank=True, null=True)
    day = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = _('Notify time options')
        verbose_name_plural = _('Notify time options')

    def __str__(self):
        ret = ''
        if self.kind is self.Kind_Instant:
            ret = _('Instantly')
        elif self.kind is self.Kind_Delayed:
            ret = _('In %d minutes') % (self.time.hour * 60 + self.time.minute)
        elif self.kind is self.Kind_Daily:
            ret = _('Everyday at %s') % self.time.strftime('%X')
        elif self.kind is self.Kind_Weekly:
            ret = _('Every %d day of week at %s') % (self.day, self.time.strftime('%X'))
        elif self.kind is self.Kind_Monthly:
            ret = _('Every %d day of month at %s') % (self.day, self.time.strftime('%X'))
        return str(ret)

    @property
    def is_instant(self):
        return self.kind is NotifyTimeOptions.Kind_Instant

    def save(self, **kwargs):
        if self.time is None and self.kind in (NotifyTimeOptions.Kind_Delayed,
                                               NotifyTimeOptions.Kind_Daily,
                                               NotifyTimeOptions.Kind_Weekly,
                                               NotifyTimeOptions.Kind_Monthly):
            raise ValidationError('time', _('This field is required for specified kind.'))

        if self.kind is NotifyTimeOptions.Kind_Weekly and self.day not in range(0, 7):
            raise ValidationError('day', _('Input day of week from 0 to 6 (0 is Sunday).'))

        if self.kind is NotifyTimeOptions.Kind_Monthly and self.day not in range(1, 28):
            raise ValidationError('day', _('Input day from 1 to 28.'))

        super().save(**kwargs)


class Notify(models.Model):
    trigger = models.ForeignKey(EventTrigger, related_name='notifiers')
    receiver_path = models.ForeignKey(EventReceiverPath)
    template_slug = models.CharField(max_length=100,
                                     validators=[validators.validate_str_placeholder],
                                     help_text=_('Template slug for single event.'
                                                 '"%s" is required for substitute language code.'))
    template_slug_mult = models.CharField(max_length=100,
                                          validators=[validators.validate_str_placeholder],
                                          help_text=_('Template slug for bundle of events (packet delivery).'
                                                      '"%s" is required for substitute language code.'))

    class Meta:
        verbose_name = _('Notify')
        verbose_name_plural = _('Notifies')
        unique_together = ('trigger', 'receiver_path')

    def __str__(self):
        return '%s #%d: "%s" -> "%s"' % (self._meta.verbose_name,
                                         self.id,
                                         self.trigger.comment or self.trigger,
                                         self.receiver_path.comment or self.receiver_path)

    def get_options_for_user(self, user_id):
        """выбираем все кастомные способы оповещения для указанного юзера + способы по умолчанию,
        для которых метод доставки не переопределён"""
        options = list(self.custom_options.filter(msa_user_id=user_id))
        custom_methods = [o.method for o in options]
        options += list(self.default_options.exclude(method__in=custom_methods))
        if not options:
            print('Warning: Notify %d has no delivery options.' % self.id)
        return options

    def push_event(self, event):
        """обрабатывает поступившее событие и принимает решение
        оповещать пользователя сразу и/или отложить"""
        receiver_id = self.receiver_path.extract_value(event)
        if receiver_id is None:
            return
        for option in self.get_options_for_user(receiver_id):
            if not option:  # не задан способ или время доставки
                continue
            if option.when.is_instant:
                self.send_notification(receiver_id, option.method, event)
            else:
                print('Warning: delayed notify option "%s" is not implemented.' % option.when)

    def send_notification(self, receiver_id, method, *events):
        """выполняет отправку оповещения для указанного пользователя указанным методом
        об указанных событиях (один или несколько) с одинаковыми app"""
        if not len(events):
            return
        if method != 'email':
            print('Warning: notify method "%s" is not implemented.' % method)
            return

        app = events[0].app
        dst = Destination.objects.get(app=app)

        profile_cache_key = dst.cas_profile_url % receiver_id
        cached_profile = cache.get(profile_cache_key)

        try:
            if not cached_profile:
                cas_url = furl(dst.cas_profile_url % receiver_id)
                cas_url.args['api_key'] = dst.cas_api_key
                cas_url = cas_url.url
                profile_responce = requests.get(cas_url)
                if profile_responce.status_code != 200:
                    print('Warning: "%s" returns %d.' % (cas_url, profile_responce.status_code))
                    return
                profile = json.loads(profile_responce.text)
                cache.set(profile_cache_key, profile, 10)  # кладём загруженный профиль в кэш на 10с
            else:
                profile = cached_profile

            language = profile.get('language')
            tz = pytz_timezone(profile.get('tz_name'))

            translation.activate(language)
            timezone.activate(tz)

            if method == 'email':
                email = profile.get('notification_email')
                if not email:
                    print('Warning: "notification_email" in "%s" not present.' % cas_url)

                single = len(events) is 1

                slug = self.template_slug if single else self.template_slug_mult
                slug %= language

                if single:
                    context = LocalizedEventSerializer(events[0]).data
                else:
                    context = LocalizedEventSerializer(events[:5],
                                                       many=True).data  # помещаем в контекст макс. 5 событий

                mailer = DBMailerAPI(dst.mailer_api_key, dst.mailer_api_url)
                mailer.send(slug, email, context)

        except ValueError:
            print('Warning: "%s" returns non-json data.' % cas_url)

        except EmailSendError:
            print('Warning: email to "%s" was not send.' % email)

        finally:
            translation.deactivate()
            timezone.deactivate()


class NotifyOptionsMixIn(models.Model):
    when = models.ForeignKey(NotifyTimeOptions, null=True, on_delete=models.SET_NULL)
    method = models.CharField(max_length=32, default='email', blank=True, null=True)  # email, sms, ...

    class Meta:
        abstract = True

    def __str__(self):
        return "%s via %s" % (self.when, self.method) if self else "(Not set)"

    def __bool__(self):
        return bool(self.when and self.method)


class DefaultNotifyOptions(NotifyOptionsMixIn):
    base = models.ForeignKey(Notify, related_name='default_options')

    class Meta:
        verbose_name = _('Default notify options')
        verbose_name_plural = _('Default notify options')
        unique_together = ('base', 'method')


class CustomNotifyOptions(NotifyOptionsMixIn):
    base = models.ForeignKey(Notify, related_name='custom_options')
    msa_user_id = models.IntegerField()

    class Meta:
        verbose_name = _('Custom notify options')
        verbose_name_plural = _('Custom notify options')
        unique_together = ('base', 'method', 'msa_user_id')
