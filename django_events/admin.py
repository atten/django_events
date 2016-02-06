from django.contrib import admin
from .models import *


class SourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'app', 'object_id', 'object_ct_id', 'created_at']

admin.site.register(Source, SourceAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'source', 'initiator', 'target', 'kind', 'context', 'timestamp']

admin.site.register(Event, EventAdmin)


class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ['label', 'key', 'is_active', 'created_at', 'allowed_origins']

admin.site.register(ApiKey, ApiKeyAdmin)
