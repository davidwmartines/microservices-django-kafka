import os
import typing

from cloudevents.kafka import (
    from_binary,
    from_structured,
    to_binary,
    to_structured,
    KafkaMessage,
)
from cloudevents.abstract import AnyCloudEvent
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer, AvroSerializer
from confluent_kafka.schema_registry.json_schema import JSONDeserializer, JSONSerializer
from confluent_kafka.serialization import (
    MessageField,
    SerializationContext,
)

from .conf import EventsConfiguration, events_conf
from .enums import CloudEventsMode, SerializationFormat

ToProtocolConverter = typing.Optional[typing.Callable[[AnyCloudEvent], KafkaMessage]]

ToCloudEventConverter = typing.Optional[typing.Callable[[KafkaMessage], AnyCloudEvent]]


_types_to_protocol_converters = {}
_types_to_event_converters = {}

_mode_to_protocol_converters = {
    CloudEventsMode.BINARY: to_binary,
    CloudEventsMode.STRUCTURED: to_structured,
}

_mode_to_event_converters = {
    CloudEventsMode.BINARY: from_binary,
    CloudEventsMode.STRUCTURED: from_structured,
}

_format_to_serializers = {
    SerializationFormat.AVRO: AvroSerializer,
    SerializationFormat.JSON: JSONSerializer,
}

_format_to_deserializers = {
    SerializationFormat.AVRO: AvroDeserializer,
    SerializationFormat.JSON: JSONDeserializer,
}

_format_mode_to_content_types = {
    SerializationFormat.AVRO: {
        CloudEventsMode.BINARY: "application/avro",
        CloudEventsMode.STRUCTURED: "application/cloudevents+avro",
    },
    SerializationFormat.JSON: {
        CloudEventsMode.BINARY: "application/json",
        CloudEventsMode.STRUCTURED: "application/cloudevents+json",
    },
}


def _get_content_type(event: AnyCloudEvent, conf: EventsConfiguration) -> str:
    type_conf = conf.types[event["type"]]
    return _format_mode_to_content_types[type_conf.format][type_conf.mode]


def _get_to_protocol_converter(
    event: AnyCloudEvent, conf: EventsConfiguration
) -> ToProtocolConverter:
    """
    Factory for getting the ToProtocolConverter for the type of event.
    """

    # see if we've already cached a converter for this type.
    converter = _types_to_protocol_converters.get(event["type"])
    if converter is not None:
        return converter

    type_conf = conf.types.get(event["type"])
    if not type_conf:
        raise KeyError(f"{event['type']} is not configured in settings.")

    # create the serializer
    if not type_conf.schema:
        raise ValueError(
            f"{event['type']} has no SCHEMA configured. Schema is required for writing."
        )
    with open(os.path.join(conf.schemas_dir, type_conf.schema)) as f:
        schema_string = f.read()
    client = SchemaRegistryClient({"url": conf.schema_registry_url})
    serializer_type = _format_to_serializers[type_conf.format]
    serializer = serializer_type(client, schema_string)

    # create the converter
    data_marshaller = lambda d: serializer(
        d, SerializationContext(type_conf.topic, MessageField.VALUE)
    )
    converter_type = _mode_to_protocol_converters[type_conf.mode]
    converter = lambda e: converter_type(e, data_marshaller=data_marshaller)

    # cache for future use
    _types_to_protocol_converters[event["type"]] = converter

    return converter


def _get_to_cloudevent_converter(
    event_type_str: str, conf: EventsConfiguration
) -> ToCloudEventConverter:
    """
    Factory function for getting the ToCloudEventConverter for the type of event.
    """

    # see if we've already cached a converter for this type
    converter = _types_to_event_converters.get(event_type_str)
    if converter is not None:
        return converter

    type_conf = conf.types.get(event_type_str)
    if not type_conf:
        # if event_type is not configured, we could parse the content-type of the
        # incoming messag to the infer mode and format.
        raise KeyError(f"{event_type_str} is not configured in settings.")

    # create the deserializer
    # reader schema is not required - deserializer will default to writer schema.
    schema_string = None
    if type_conf.schema:
        with open(os.path.join(conf.schemas_dir, type_conf.schema)) as f:
            schema_string = f.read()
    client = SchemaRegistryClient({"url": conf.schema_registry_url})
    deserializer_type = _format_to_deserializers[type_conf.format]
    deserializer = deserializer_type(client, schema_string)

    # create the converter
    converter_type = _mode_to_event_converters[type_conf.mode]
    data_unmarshaller = lambda d: deserializer(
        d, SerializationContext(type_conf.topic, MessageField.VALUE)
    )
    converter = lambda e: converter_type(e, data_unmarshaller=data_unmarshaller)

    # cache for future use
    _types_to_event_converters[event_type_str] = converter

    return converter


def to_protocol(event: AnyCloudEvent) -> KafkaMessage:
    """
    Converts a CloudEvent to a Kafka Protocol Message object.
    """
    conf = events_conf()
    converter = _get_to_protocol_converter(event, conf)
    # ensure the content-type is set.
    if "content-type" not in event:
        event["content-type"] = _get_content_type(event, conf)
    return converter(event)


def to_cloudevent(message: KafkaMessage, event_name: str) -> AnyCloudEvent:
    """
    Converts a Kafka Protocol Message to a CloudEvent.
    """
    conf = events_conf()
    converter = _get_to_cloudevent_converter(event_name, conf)
    return converter(message)
