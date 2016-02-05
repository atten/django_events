from rest_framework import serializers
from .models import *


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('name', 'label', 'object_id', 'object_ct_id', 'created_at')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('source', 'initiator', 'target', 'kind', 'context', 'timestamp')
