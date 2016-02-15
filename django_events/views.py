from rest_framework import viewsets, mixins, permissions
from .serializers import *
from .models import *


class HasValidApiKeyOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        try:
            val = request.GET.get('api_key') or request.data.get('api_key')
            app = ApiKey.objects.get(key=val, is_active=True).app
            request.app = app       # put found app to request (will be extracted in EventSerializer and EventViewSet)
            return True
        except (ApiKey.DoesNotExist, ValueError):
            return False


class EventViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (HasValidApiKeyOrAdmin,)
    filter_fields = ('scope',)

    def get_queryset(self):
        queryset = self.queryset

        if hasattr(self.request, 'app'):
            queryset = queryset.filter(source__app=self.request.app)

        return queryset
