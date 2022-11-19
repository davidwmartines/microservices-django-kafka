import logging
import os
import typing
from abc import ABC, abstractmethod

from cloudevents.abstract import AnyCloudEvent
from cloudevents.kafka import KafkaMessage
from confluent_kafka import Message
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import MessageField, SerializationContext

from .conversion import to_cloudevent

from .conf import events_conf

logger = logging.getLogger(__name__)


def _get_headers(message: Message) -> typing.Dict[str, bytes]:
    headers_list = message.headers()
    if headers_list:
        return {h[0]: h[1] for h in headers_list}
    return {}


class CloudEventHandler(ABC):
    """
    Base class for handlers of CloudEvents-spec compliant event messages from Kafka.

    CloudEventHandler instances are Callable.
    """

    def __init__(self, event_name: str) -> None:
        assert event_name
        self._event_name = event_name

    @abstractmethod
    def handle(self, event: AnyCloudEvent) -> None:
        """
        Template method for subclasses to perform their handling of specific event types.

        Arguments:
            event (Event): a deserialized Event instance.  Handlers will typically use the `data` attribute
            to access the event-type sepcific payload.
        """
        raise NotImplementedError()

    def __call__(self, message: Message) -> None:
        """
        Callable interface.

        Arguments:
            message (Message): a Kafka Client message instance.
        """
        logger.debug(
            f"handling message key {message.key().decode()} topic {message.topic()}"
        )

        event = to_cloudevent(
            KafkaMessage(
                _get_headers(message), key=message.key().decode(), value=message.value()
            ),
            self._event_name,
        )

        logger.debug(
            f"successfully deserialized {event['type']} event id {event['id']} from {event['source']}."
        )

        self.handle(event)

        logger.info(f"event {event['id']} was handled")


class GenericEventHandler(ABC):
    """
    Base class for handlers of non-cloudevent messages from Kafka.

    GenericEventHandler instances are Callable.
    """

    @abstractmethod
    def handle(self, data: dict, headers: dict) -> None:
        """
        Template method for subclasses to perform their handling of specific event types.

        Arguments:
            data (dict): a deserialized dictionary of the event payload.
            headers (dict): a dictionary of the incoing message headers.
        """
        raise NotImplementedError()

    def __init__(
        self, deserializer_type: type = AvroDeserializer, schema_file_name: str = None
    ) -> None:

        conf = events_conf()

        schema_string = None
        if schema_file_name:
            with open(
                os.path.join(
                    conf.schemas_dir,
                    self.schema_file_name,
                )
            ) as f:
                schema_string = f.read()

        schema_registry_client = SchemaRegistryClient({"url": conf.schema_registry_url})

        self._deserializer = deserializer_type(
            schema_registry_client, schema_str=schema_string
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

        data = self._deserializer(
            message.value(),
            SerializationContext(message.topic(), MessageField.VALUE),
        )

        logger.debug("successfully deserialized message")

        self.handle(data, _get_headers(message))

        logger.info("message was handled")
