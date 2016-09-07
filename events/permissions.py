from rest_framework import permissions

from .models import ApiKey


class HasValidApiKey(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            val = request.GET.get('api_key') or request.data.get('api_key')
            app = ApiKey.objects.get(key=val, is_active=True).app
            request.app = app       # put found app to request
            return True
        except (ApiKey.DoesNotExist, ValueError):
            return False
