from typing import Callable, NamedTuple

from django.db import transaction

from events.models import OutboxItem
from events.serializers import EventSerializer

from . import create_event


class Config(NamedTuple):
    """
    Defines the configuration properties for creating events
    from model instances using save_event decorator.
    """

    schema: str
    """
    Name of the schema to use.
    """

    topic: str
    """
    The topic name (subject) the schema will be registred to.
    """

    event_type: str
    """
    The type of event to generate.
    """

    to_dict: Callable[[object], dict]
    """
    Function that takes a model and returns a dictionary
    matching the data payload of the target schema.
    """


def save_event(config: Config):
    """
    Decorates a model's save method to include
    transactionally saving an event to the outbox table.

    Arguments:
        config (Config): a config object that specifies how to create events from the model on save.

    Note:
        Inspired by https://github.com/juntossomosmais/django-outbox-pattern
    """

    def save(self, *args, **kwargs):
        # Note, the event and outbox item are created before the transaction begins.
        # This is so that the serialization is not happening during the db transaction.
        # The serialization process may need to make an API call to Schema-Registry on the
        # first invocation to get/register the schema, and we don't want that IO to be blocking
        # the transaction.
        # The downside is that we don't have access to the model fields that are generated
        # at save time such as as created and modified.
        # If the serialization could be optimized to not require any IO, the creation of the
        # event and outbox item could be moved inside the transaction, after saving the model.
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
        serializer = EventSerializer(schema=config.schema, topic=config.topic)
        _serializers[config.schema] = serializer

    event = create_event(config.event_type, config.to_dict(model))

    return OutboxItem.from_event(
        event, topic=config.topic, key=model.pk, serializer=serializer
    )
