from django.db import models
from django.contrib.postgres.fields import JSONField


class Stream(models.Model):
    label = models.CharField(max_length=70)
    project = models.CharField(max_length=50)
    app = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField(default=0)
    object_ct_id = models.PositiveIntegerField(default=0)
    header_template = models.TextField(max_length=50)
    body_template = models.TextField(max_length=50)


class StreamEvent(models.Model):
    stream = models.ForeignKey(Stream, related_name="events")
    data = JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=70)
    target = models.CharField(max_length=70)


# class UserStream(models.Model):
#     stream = models.ForeignKey(Stream)
#     user = models.ForeignKey(User)
#     transports = BitField()
