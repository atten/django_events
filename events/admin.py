from django.contrib import admin
from .models import *


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'app', 'context', 'timestamp']

admin.site.register(Event, EventAdmin)


class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ['key', 'app', 'is_active', 'created_at']

admin.site.register(ApiKey, ApiKeyAdmin)
