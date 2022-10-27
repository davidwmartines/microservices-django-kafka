from django.db import transaction

from events.models import OutboxItem
from events.serializers import EventSerializer

from . import Config, create_event


def save_event(config: Config):
    """
    Decorates a model's save method to include
    transactionally saving an event to the outbox table.

    Inspired by https://github.com/juntossomosmais/django-outbox-pattern
    """

    def save(self, *args, **kwargs):
        outbox_item = _create_outbox_item(self, config)
        with transaction.atomic():
            super(self.__class__, self).save(*args, **kwargs)
            outbox_item.save()

    def decorator_save_event(cls):
        cls.save = save
        return cls

    return decorator_save_event


_serializers = {}


def _create_outbox_item(model: object, config: Config) -> OutboxItem:
    serializer = _serializers.get(config.schema)
    if not serializer:
        serializer = EventSerializer(config)
        _serializers[config.schema] = serializer

    event = create_event("entity.saved", config.to_dict(model))

    return OutboxItem.from_event(
        event, topic=config.topic, key=model.pk, serializer=serializer
    )
