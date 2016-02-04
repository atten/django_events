from rest_framework import serializers
from .models import *


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('object_id', 'object_ct_id', 'name', 'project', 'app', 'created_at')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('source', 'initiator', 'target', 'type', 'args', 'timestamp')
