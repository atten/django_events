from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
import uuid


class Source(models.Model):
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=100)    # app.model
    object_id = models.PositiveIntegerField(default=0)
    object_ct_id = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    # header_template = models.TextField(max_length=50)
    # body_template = models.TextField(max_length=50)

    # def __str__(self):
    #     return "Source '%s' <%s:%d>" % (self.name, self.label, self.object_id)


class Event(models.Model):
    EVENT_KINDS = (
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
    kind = models.SmallIntegerField(choices=EVENT_KINDS)
    context = JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return 'Event:%d' % self.id


class ApiKey(models.Model):
    key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=64, blank=True, default='Default')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    allowed_origins = models.TextField(blank=True, default='127.0.0.1', help_text=_('List of IP addresses'))

    # def get_audit_log_data(self):
    #     return {
    #         'label': self.label,
    #         'key': self.key,
    #         'is_active': self.is_active,
    #     }
