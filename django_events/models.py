from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
import uuid


class Source(models.Model):
    app = models.CharField(max_length=100, default="default")
    content_type = models.PositiveIntegerField()
    # header_template = models.TextField(max_length=50)
    # body_template = models.TextField(max_length=50)

    class Meta:
        unique_together = (('app', 'content_type'),)

    def __str__(self):
        return "Source %s:%d" % (self.app, self.content_type)


class Event(models.Model):
    EVENT_KINDS = (
        (0, _('Other')),
        (1, _('Create')),
        (2, _('Change')),
        (3, _('Remove')),
        (4, _('Clear')),
        (5, _('Reset')),
    )

    source = models.ForeignKey(Source, related_name="events")
    initiator = models.ForeignKey(Source, related_name="events_initiated_by")
    target = models.ForeignKey(Source, related_name="events_targeted_to", blank=True, null=True)
    kind = models.SmallIntegerField(choices=EVENT_KINDS)
    context = JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    # def __str__(self):
    #     return 'Event:%d' % self.id


class ApiKey(models.Model):
    key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=100, blank=True, null=True)
    app = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    allowed_origins = models.TextField(blank=True, default='127.0.0.1', help_text=_('List of IP addresses'))

    # def get_audit_log_data(self):
    #     return {
    #         'label': self.label,
    #         'key': self.key,
    #         'is_active': self.is_active,
    #     }
