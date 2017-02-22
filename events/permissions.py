from rest_framework import permissions

from .models import ApiKey


class HasValidApiKey(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            val = request.META.get('HTTP_API_KEY')
            app = ApiKey.objects.get(key=val, is_active=True).app
            request.app = app       # put found app to request
            return True
        except (ApiKey.DoesNotExist, ValueError):
            return False
