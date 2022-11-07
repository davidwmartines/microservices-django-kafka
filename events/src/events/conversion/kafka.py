import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Tuple

from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import MessageField, SerializationContext

from .. import Event
from ..conf import EventsConfiguration, events_conf
from ..enums import CloudEventsMode, SerializationFormat
from . import EventConverter, ProtocolEvent


@dataclass
class KafkaEvent(ProtocolEvent):
    key: str or bytes
    topic: str
    headers: dict


def _get_serializer_type(format: SerializationFormat) -> type:
    if format == SerializationFormat.AVRO:
        return AvroSerializer
    elif format == SerializationFormat.JSON:
        raise NotImplementedError()


def _get_content_type_header(format: SerializationFormat, mode: CloudEventsMode) -> str:
    if mode == CloudEventsMode.BINARY and format == SerializationFormat.AVRO:
        return "application/avro"
    elif mode == CloudEventsMode.STRUCTURED and format == SerializationFormat.AVRO:
        return "applcation/cloudevents+avro"
    elif mode == CloudEventsMode.BINARY and format == SerializationFormat.JSON:
        return "application/json"
    elif mode == CloudEventsMode.STRUCTURED and format == SerializationFormat.JSON:
        return "applcation/cloudevents+json"
    else:
        raise NotImplementedError()


def _load_schema_string(file_name: str, conf: EventsConfiguration) -> str:
    with open(os.path.join(conf.schemas_dir, file_name)) as f:
        return f.read()


_serializers = {}


class KafkaEventConverter(ABC, EventConverter):
    @abstractmethod
    def _get_body_and_headers(
        self,
        event: Event,
        conf: EventsConfiguration,
        to_dict: Callable[[object], dict] = None,
    ) -> Tuple[dict, dict]:
        raise NotImplementedError()

    def __call__(
        self,
        event: Event,
        to_dict: Callable[[object], dict] = None,
        key_mapper: Callable[[Event], str or bytes] = None,
        *args,
        **kwargs
    ) -> KafkaEvent:

        assert event

        conf = events_conf()

        # resolve options
        event_type_conf = conf.types.get(event.type)
        schema = kwargs.get("schema", event_type_conf.schema)
        topic = kwargs.get("topic", event_type_conf.topic)
        format = kwargs.get("format", event_type_conf.format)
        mode = kwargs.get("mode", event_type_conf.mode)

        serializer = _serializers.get(schema)
        if not serializer:
            client = SchemaRegistryClient({"url": conf.schema_registry_url})
            schema_string = _load_schema_string(schema, conf)
            serializer_type = _get_serializer_type(format)
            serializer = serializer_type(client, schema_string)
            _serializers[schema] = serializer

        body, headers = self._get_body_and_headers(event, conf, to_dict)

        value = serializer(body, SerializationContext(topic, MessageField.VALUE))

        headers["content-type"] = _get_content_type_header(format, mode)

        if key_mapper:
            key = key_mapper(event)
        else:
            key = None

        return KafkaEvent(event, value, key, topic, headers)


class BinaryKafkaEventConverter(KafkaEventConverter):
    def _get_body_and_headers(
        self,
        event: Event,
        conf: EventsConfiguration,
        to_dict: Callable[[object], dict] = None,
    ) -> Tuple[dict, dict]:

        if to_dict:
            body = to_dict(event.data)
        else:
            if not isinstance(event.data, dict):
                raise TypeError(
                    "Event.data must be a dict, or else supply a to_dict function"
                )
            body = event.data

        headers = {
            "ce_specversion": "1.0",
            "ce_id": str(event.id),
            "ce_type": event.type,
            "ce_time": event.time.isoformat(),
            "ce_source": conf.event_source_name,
        }

        return body, headers
