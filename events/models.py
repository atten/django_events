from django.db import models
from django.contrib.postgres.fields import JSONField
import uuid


class Event(models.Model):
    app = models.CharField(max_length=100)
    context = JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    # def __str__(self):
    #     return 'Event:%d' % self.id


class ApiKey(models.Model):
    key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    app = models.CharField(max_length=100)
    # allowed_origins = models.TextField(blank=True, default='127.0.0.1', help_text=_('List of IP addresses'))
