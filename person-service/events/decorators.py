from uuid import uuid4

from django.db import transaction

from events.models import Event
from events.serializers import EventSerializer

from . import Config, create_event


def save_event(config: Config):
    """
    Decorates a model's save method to include
    transactionally saving an event to the outbox table.

    Inspired by https://github.com/juntossomosmais/django-outbox-pattern
    """

    def save(self, *args, **kwargs):
        outbox_event = _create_outbox_event(self, config)
        with transaction.atomic():
            super(self.__class__, self).save(*args, **kwargs)
            outbox_event.save()

    def decorator_save_event(cls):
        cls.save = save
        return cls

    return decorator_save_event


_serializers = {}


def _create_outbox_event(model: object, config: Config) -> Event:
    serializer = _serializers.get(config.schema)
    if not serializer:
        serializer = EventSerializer(config)
        _serializers[config.schema] = serializer

    event = create_event("entity.saved", config.to_dict(model))
    payload = serializer(event)

    outbox_event = Event(
        id=uuid4(),
        aggregatetype=model.__class__.__name__,
        aggregateid=model.pk,
        timestamp=event.time,
        event_type=event.event_type,
        source=event.source,
        content_type="application/avro",
        payload=payload,
    )
    return outbox_event
