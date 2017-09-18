from django.db.models import Q
from rest_framework import viewsets, mixins

from events.serializers import MultiSerializerViewSetMixin
from . import serializers
from .models import Event


class EventViewSet(MultiSerializerViewSetMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Event.objects.all()

    serializer_class = serializers.EventSerializer
    serializer_action_classes = {
        'create': serializers.FullEventSerializer,
        'update': serializers.FullEventSerializer,
        'partial_update': serializers.FullEventSerializer,
    }

    filter_fields = ('context', 'timestamp')

    def create(self, request, *args, **kwargs):
        request.data['app'] = request.app
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.request, 'app'):
            queryset = queryset.filter(app=self.request.app)

        scopes = self.request.GET.get('scope').split(',')
        qu = Q()
        for scope in scopes:
            qu |= Q(context__scope=scope)
        queryset = queryset.filter(qu)

        return queryset
