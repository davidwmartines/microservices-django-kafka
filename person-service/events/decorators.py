from datetime import datetime
from uuid import uuid4

from django.utils import timezone
from django.db import transaction

from events.models import Event
from events.serializers import EventSerializer

from . import Config


def save_event(config: Config):
    """
    Decorates a model's save method to include
    transactionally saving an event to the outbox table.

    Inspired by https://github.com/juntossomosmais/django-outbox-pattern
    """

    def save(self, *args, **kwargs):
        event = _create_event(self, config)
        with transaction.atomic():
            super(self.__class__, self).save(*args, **kwargs)
            event.save()

    def decorator_publish(cls):
        cls.save = save
        return cls

    return decorator_publish


_serializers = {}


def _create_event(obj: object, config: Config) -> Event:
    serializer = _serializers.get(config.schema)
    if not serializer:
        serializer = EventSerializer(config)
        _serializers[config.schema] = serializer

    payload = serializer(obj)

    return Event(
        id=uuid4(),
        aggregatetype=obj.__class__.__name__,
        aggregateid=obj.pk,
        timestamp=timezone.now(),
        type="save",
        payload=payload,
    )
