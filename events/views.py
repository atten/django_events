from rest_framework import viewsets, mixins
from rest_framework.serializers import ModelSerializer

from . import serializers
from .models import Event


class SafeModelSerializerMixIn(object):
    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            orig_model = self.serializer_class.Meta.model

            class CreateInstanceSerializer(ModelSerializer):
                class Meta:
                    model = orig_model

            return CreateInstanceSerializer

        return self.serializer_class


class EventViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   SafeModelSerializerMixIn,
                   viewsets.GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer
    filter_fields = ('context', 'timestamp')

    def create(self, request, *args, **kwargs):
        request.data['app'] = request.app
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.request, 'app'):
            queryset = queryset.filter(app=self.request.app)

        scope = self.request.GET.get('context__scope__in')
        if scope:
            queryset = queryset.filter(context__scope=scope)

        return queryset
