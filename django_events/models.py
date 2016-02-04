from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
import uuid


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
    params = JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Event:%d' % self.id


# class UserStream(models.Model):
#     stream = models.ForeignKey(Stream)
#     user = models.ForeignKey(User)
#     transports = BitField()


class ApiKey(models.Model):
    key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=64, blank=True, default='Default')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    allowed_origins = models.TextField(blank=True, default='127.0.0.1', help_text=_('List of IP addresses'))

    # def validate(self, origin):
    #     if not self.allowed_origins:
    #         return False
    #     origins = self.allowed_origins.split('\n')
    #     return origin in origins
    #
    # def get_audit_log_data(self):
    #     return {
    #         'label': self.label,
    #         'key': self.key,
    #         'is_active': self.is_active,
    #     }
