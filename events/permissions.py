from rest_framework import permissions
from rest_framework.request import Request

from .models import ApiKey


class ValidApiKeyOrDenied(permissions.BasePermission):
    def has_permission(self, request: Request, view):
        try:
            app = ApiKey.objects.get(key=request.META.get('HTTP_API_KEY'), is_active=True).app
            request.app = app  # put found app to request
            return True
        except (ApiKey.DoesNotExist, ValueError):
            return False


class ValidApiKeyOrSuperuserOrDenied(ValidApiKeyOrDenied):
    def has_permission(self, request: Request, view: callable) -> bool:
        return request.user.is_superuser or super().has_permission(request, view)
