from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4


class Source(models.Model):
    name = models.CharField(max_length=70)
    project = models.CharField(max_length=50)
    app = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField(default=0)
    object_ct_id = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    # header_template = models.TextField(max_length=50)
    # body_template = models.TextField(max_length=50)

    def __str__(self):
        return 'Source:%d <%s.%s.%s>' % (self.id, self.project, self.app, self.name)


class Event(models.Model):
    EVENT_TYPES = (
        (0, _('Other')),
        (1, _('Change')),
        (2, _('Add')),
        (3, _('Remove')),
        (4, _('Clear')),
        (5, _('Reset')),
    )

    source = models.ForeignKey(Source, related_name="events")
    initiator = models.ForeignKey(Source, related_name="events_initiated_by")
    target = models.ForeignKey(Source, related_name="events_targeted_to")
    type = models.SmallIntegerField(choices=EVENT_TYPES)
    args = JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Event:%d' % self.id


# class UserStream(models.Model):
#     stream = models.ForeignKey(Stream)
#     user = models.ForeignKey(User)
#     transports = BitField()


class ApiKey(models.Model):
    label = models.CharField(max_length=64, blank=True, default='Default')
    key = models.CharField(max_length=32, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    allowed_origins = models.TextField(blank=True, null=True)

    @classmethod
    def generate_api_key(cls):
        return uuid4().hex

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = ApiKey.generate_api_key()
        super(ApiKey, self).save(*args, **kwargs)

    def get_allowed_origins(self):
        if not self.allowed_origins:
            return []
        return filter(bool, self.allowed_origins.split('\n'))

    def get_audit_log_data(self):
        return {
            'label': self.label,
            'key': self.key,
            'is_active': self.is_active,
        }
