from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'notifications'

    def ready(self):
        from .import signals
