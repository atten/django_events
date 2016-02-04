from rest_framework import viewsets, mixins, permissions
from .serializers import *
from .models import *


class HasValidApiKey(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            val = request.GET['api_key'] or request.data['api_key']
            ip_addr = request.META['REMOTE_ADDR']
            ApiKey.objects.get(key=val, is_active=True, allowed_origins__icontains=ip_addr)
            return True
        except ApiKey.DoesNotExist:
            return False


class SourceViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = (HasValidApiKey,)


class EventViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (HasValidApiKey,)
