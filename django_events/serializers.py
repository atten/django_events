from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import *


class SourceField(serializers.RelatedField):
    queryset = Source.objects.all()

    def to_representation(self, value):
        return '%s:%s' % (value.object_ct_id, value.object_id)

    def to_internal_value(self, data):
        ct_id, id = data.split(':')
        kwargs = {'object_id': id, 'object_ct_id': ct_id}
        try:
            return self.get_queryset().get(**kwargs)
        except ObjectDoesNotExist:
            return Source.objects.create(**kwargs)


class EventSerializer(serializers.ModelSerializer):
    source = SourceField()
    target = SourceField()
    initiator = SourceField()

    class Meta:
        model = Event
        fields = ('source', 'initiator', 'target', 'kind', 'context', 'timestamp')
