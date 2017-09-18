from datetime import timedelta

from django.utils.dateparse import parse_datetime
from django.utils.formats import localize
from rest_framework import serializers

from .models import Event
from .utils import localize_duration, localize_timedelta


class MultiSerializerViewSetMixin:
    def get_serializer_class(self, action=None):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.

        Thanks gonz: http://stackoverflow.com/a/22922156/11440

        """
        try:
            return self.serializer_action_classes[action or self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('context', 'timestamp')


class FullEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class LocalizedEventSerializer(EventSerializer):
    context = serializers.SerializerMethodField()

    @staticmethod
    def get_context(obj):
        ret = {}
        for key, val in obj.context.items():
            if key in ('start', 'end'):
                val = localize(parse_datetime(val).astimezone())
            elif key == 'duration' and len(val) == 2:
                val = localize_duration(parse_datetime(val[0]).astimezone(), parse_datetime(val[1]).astimezone())
            elif key == 'timedelta':
                val = localize_timedelta(timedelta(seconds=float(val)))
            ret[key] = val
        return ret

    class Meta:
        model = Event
        fields = ('context', 'timestamp')
