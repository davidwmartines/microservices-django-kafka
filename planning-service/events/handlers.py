import logging
import os
from abc import ABC, abstractmethod

from confluent_kafka import Message
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import MessageField, SerializationContext
from django.conf import settings

from events import Event, dict_to_event

logger = logging.getLogger(__name__)


class EventHandler(ABC):
    @abstractmethod
    def schema_file_name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def handle(self, event: Event) -> None:
        raise NotImplementedError()

    def __init__(self) -> None:

        with open(
            os.path.join(
                settings.BASE_DIR, settings.EVENTS_SCHEMAS_DIR, self.schema_file_name()
            )
        ) as f:
            schema_string = f.read()

        schema_registry_client = SchemaRegistryClient(
            {"url": settings.SCHEMA_REGISTRY_URL}
        )

        self.deserializer = AvroDeserializer(
            schema_registry_client, schema_string, dict_to_event
        )

    def __call__(self, message: Message) -> None:
        logger.debug(
            f"handling message key {message.key().decode()} topic {message.topic()}"
        )
        event = self.deserializer(
            message.value(), SerializationContext(message.topic(), MessageField.VALUE)
        )
        logger.debug(
            f"successfully deserialized {event.event_type} event id {event.id} from {event.source}."
        )
        self.handle(event)
        logger.info(f"event {event.id} was handled")
