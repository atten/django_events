from django.db.models.signals import post_save
from django.dispatch import receiver

from events.models import Event
from .models import EventTrigger


@receiver(post_save, sender=Event)
def on_create_event(sender, instance, created, **kwargs):
    if created:
        process_triggers(instance)


def process_triggers(event):
    for trigger in EventTrigger.objects.matches(event):
        for notify in trigger.notifiers.all():
            notify.push_event(event)
