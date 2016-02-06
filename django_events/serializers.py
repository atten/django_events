from rest_framework import serializers
from .models import *


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('source', 'initiator', 'target', 'kind', 'context', 'timestamp')
