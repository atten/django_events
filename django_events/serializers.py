from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import *


class SourceField(serializers.RelatedField):
    queryset = Source.objects.all()

    def to_representation(self, value):
        return value.content_type

    def to_internal_value(self, data):
        kwargs = {'content_type': data}

        request = self.context['request']
        if hasattr(request, 'app'):
            kwargs['app'] = request.app

        try:
            return self.get_queryset().get(**kwargs)
        except ObjectDoesNotExist:
            return Source.objects.create(**kwargs)


class EventSerializer(serializers.ModelSerializer):
    source = SourceField()
    target = SourceField(required=False, allow_null=True, default=None)
    initiator = SourceField()

    class Meta:
        model = Event
        fields = ('source', 'initiator', 'target', 'kind', 'context', 'timestamp')
