from django.contrib import admin
from .models import *


class SourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'app', 'content_type']

admin.site.register(Source, SourceAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'source', 'initiator', 'target', 'kind', 'scope', 'context', 'timestamp']

admin.site.register(Event, EventAdmin)


class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ['key', 'app', 'label', 'is_active', 'created_at']

admin.site.register(ApiKey, ApiKeyAdmin)
