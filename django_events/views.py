from rest_framework import viewsets, mixins, permissions, response
from .serializers import *
from .models import *


class HasValidApiKeyOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        try:
            val = request.GET.get('api_key') or request.data.get('api_key')
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
    permission_classes = (HasValidApiKeyOrAdmin,)


class EventViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (HasValidApiKeyOrAdmin,)

    def get_queryset(self):
        queryset = Event.objects.all()
        d = self.request.query_params

        source = d.get('source')
        if source is not None:
            queryset = queryset.filter(source=source)

        initiator = d.get('initiator')
        if initiator is not None:
            queryset = queryset.filter(initiator=initiator)

        target = d.get('target')
        if target is not None:
            queryset = queryset.filter(target=target)

        return queryset
