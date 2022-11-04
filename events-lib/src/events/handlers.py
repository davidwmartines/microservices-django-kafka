import logging
import os
from abc import ABC, abstractmethod
from typing import Any
from confluent_kafka import Message
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import MessageField, SerializationContext
from django.conf import settings

from events import Event, dict_to_event

logger = logging.getLogger(__name__)


class EventHandler(ABC):
    """
    Base class for handlers of Avro-serialized, CloudEvents-spec compliant event messages from Kafka.

    EventHandler instances are Callable.
    """

    schema_file_name: str = None
    """
    Allows using an explicit reader-schema for deserialization
    by specifying the file name of an avro schema.
    If None, the writer-schema of the incoming message will be
    used for deserialization.
    """

    def from_dict(self, val: dict, *args: Any) -> Any:
        """
        Converts the incoming deserialized dictionary into an Event instance or other object.
        The default behavior is to create an Event object, based on the CloudEvents spec event model.
        Subclasses can override this depending on the structure of the event recieved.
        """
        return dict_to_event(val, *args)

    @abstractmethod
    def handle(self, event: Event or object) -> None:
        """
        Template method for subclasses to perform their handling of specific event types.

        Arguments:
            event (Event): a deserialized Event instance.  Handlers will typically use the `data` field
            to access the event-type sepcific payload.
        """
        raise NotImplementedError()

    def __init__(self) -> None:

        schema_string = None

        if self.schema_file_name:
            with open(
                os.path.join(
                    settings.BASE_DIR,
                    settings.EVENTS_SCHEMAS_DIR,
                    self.schema_file_name,
                )
            ) as f:
                schema_string = f.read()

        schema_registry_client = SchemaRegistryClient(
            {"url": settings.SCHEMA_REGISTRY_URL}
        )

        self.deserializer = AvroDeserializer(
            schema_registry_client, schema_str=schema_string, from_dict=self.from_dict
        )

    def __call__(self, message: Message) -> None:
        """
        Callable interface.

        Arguments:
            message (Message): a Kafka Client message instance.
        """
        logger.debug(
            f"handling message key {message.key().decode()} topic {message.topic()}"
        )
        event = self.deserializer(
            message.value(), SerializationContext(message.topic(), MessageField.VALUE)
        )
        if isinstance(event, Event):
            logger.debug(
                f"successfully deserialized {event.event_type} event id {event.id} from {event.source}."
            )
        else:
            logger.debug("successfully deserialized message")

        self.handle(event)

        if isinstance(event, Event):
            logger.info(f"event {event.id} was handled")
        else:
            logger.info("message was handled")
