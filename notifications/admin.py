from django.contrib import admin
from .models import *


class DestinationAdmin(admin.ModelAdmin):
    list_display = ['id', 'app', 'mailer_api_url', 'mailer_api_key', 'cas_profile_url', 'cas_api_key']

admin.site.register(Destination, DestinationAdmin)


class EventTriggerAdmin(admin.ModelAdmin):
    list_display = ['id', 'app', 'lookup_kwargs', 'comment']

admin.site.register(EventTrigger, EventTriggerAdmin)


class EventReceiverPathAdmin(admin.ModelAdmin):
    list_display = ['id', 'path', 'comment']

admin.site.register(EventReceiverPath, EventReceiverPathAdmin)


class NotifyTimeOptionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'kind', 'time', 'day']

admin.site.register(NotifyTimeOptions, NotifyTimeOptionsAdmin)


class NotifyAdmin(admin.ModelAdmin):
    list_display = ['id', 'trigger', 'receiver_path', 'template_slug', 'template_slug_mult']

admin.site.register(Notify, NotifyAdmin)


class DefaultNotifyOptionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'base', 'when', 'method']

admin.site.register(DefaultNotifyOptions, DefaultNotifyOptionsAdmin)


class CustomNotifyOptionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'base', 'when', 'method', 'msa_user_id']

admin.site.register(CustomNotifyOptions, CustomNotifyOptionsAdmin)
