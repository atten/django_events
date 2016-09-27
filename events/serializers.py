from datetime import timedelta
from rest_framework import serializers
from django.utils.dateparse import parse_datetime
from django.utils.formats import localize

from .models import Event
from .utils import localize_duration, localize_timedelta


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('context', 'timestamp')


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
