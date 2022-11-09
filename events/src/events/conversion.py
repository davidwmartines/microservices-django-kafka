import os
import typing

from cloudevents import kafka
from cloudevents.abstract import AnyCloudEvent
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer, AvroSerializer
from confluent_kafka.schema_registry.json_schema import JSONDeserializer, JSONSerializer
from confluent_kafka.serialization import (
    MessageField,
    SerializationContext,
    Serializer,
    Deserializer,
)

from .conf import EventsConfiguration, events_conf
from .enums import CloudEventsMode, SerializationFormat

ToProtocolConverter = typing.Optional[typing.Callable[[AnyCloudEvent], typing.Any]]

ToCloudEventConverter = typing.Optional[typing.Callable[[typing.Any], AnyCloudEvent]]


_types_to_protocol_converters = {}
_types_to_event_converters = {}

_mode_to_protocol_converters = {
    CloudEventsMode.BINARY: kafka.to_binary,
    CloudEventsMode.STRUCTURED: kafka.to_structured,
}

_mode_to_event_converters = {
    CloudEventsMode.BINARY: kafka.from_binary,
    CloudEventsMode.STRUCTURED: kafka.from_structured,
}

_format_to_serializers = {
    SerializationFormat.AVRO: AvroSerializer,
    SerializationFormat.JSON: JSONSerializer,
}

_format_to_deserializers = {
    SerializationFormat.AVRO: AvroDeserializer,
    SerializationFormat.JSON: JSONDeserializer,
}

_format_to_content_types = {
    SerializationFormat.AVRO: "application/avro",
    SerializationFormat.JSON: "application/json",
}


def _get_content_type(event: AnyCloudEvent, conf: EventsConfiguration) -> str:
    type_conf = conf.types[event["type"]]
    base_type = _format_to_content_types[type_conf.format]
    if type_conf.mode == CloudEventsMode.STRUCTURED:
        return base_type + "+cloudevents"
    else:
        return base_type


def _create_serializer(event: AnyCloudEvent, conf: EventsConfiguration) -> Serializer:
    type_conf = conf.types[event["type"]]
    if not type_conf.schema:
        raise ValueError(
            f"{event['type']} has no SCHEMA configured in settings. Schema is required for writing."
        )
    with open(os.path.join(conf.schemas_dir, type_conf.schema)) as f:
        schema_string = f.read()
    client = SchemaRegistryClient({"url": conf.schema_registry_url})
    serializer_type = _format_to_serializers[type_conf.format]
    return serializer_type(client, schema_string)


def _create_deserializer(type: str, conf: EventsConfiguration) -> Deserializer:
    type_conf = conf.types[type]
    # reader schema is not required.  Deserializer will default to writer schema.
    schema_string = None
    if type_conf.schema:
        with open(os.path.join(conf.schemas_dir, type_conf.schema)) as f:
            schema_string = f.read()
    client = SchemaRegistryClient({"url": conf.schema_registry_url})
    deserializer_type = _format_to_deserializers[type_conf.format]
    return deserializer_type(client, schema_string)


def _get_to_protocol_converter(
    event: AnyCloudEvent, conf: EventsConfiguration
) -> ToProtocolConverter:
    """
    Factory function for getting the ToProtocolConverter for the type of event.
    """

    converter = _types_to_protocol_converters.get(event["type"])
    if converter is not None:
        return converter

    type_conf = conf.types.get(event["type"])
    if not type_conf:
        raise KeyError(f"{event['type']} is not configured in settings.")

    converter_type = _mode_to_protocol_converters[type_conf.mode]
    serializer = _create_serializer(event, conf)
    data_marshaller = lambda d: serializer(
        d, SerializationContext(type_conf.topic, MessageField.VALUE)
    )
    converter = lambda e: converter_type(e, data_marshaller=data_marshaller)

    _types_to_protocol_converters[event["type"]] = converter

    return converter


def _get_to_cloudevent_converter(
    event_type_str: str, conf: EventsConfiguration
) -> ToCloudEventConverter:
    """
    Factory function for getting the ToCloudEventConverter for the type of event.
    """
    converter = _types_to_event_converters.get(event_type_str)
    if converter is not None:
        return converter

    type_conf = conf.types.get(event_type_str)
    if not type_conf:
        raise KeyError(f"{event_type_str} is not configured in settings.")

    converter_type = _mode_to_event_converters[type_conf.mode]
    deserializer = _create_deserializer(event_type_str, conf)
    data_unmarshaller = lambda d: deserializer(
        d, SerializationContext(type_conf.topic, MessageField.VALUE)
    )
    converter = lambda e: converter_type(e, data_unmarshaller=data_unmarshaller)

    _types_to_event_converters[event_type_str] = converter

    return converter


def to_protocol(event: AnyCloudEvent) -> kafka.ProtocolMessage:
    """
    Converts a CloudEvent to a Kafka Protocol Message object.
    """
    conf = events_conf()
    converter = _get_to_protocol_converter(event, conf)
    event["content-type"] = _get_content_type(event, conf)
    return converter(event)


def to_cloudevent(message: kafka.ProtocolMessage, event_name: str) -> AnyCloudEvent:
    """
    Converts a Kafka Protocol Message to a CloudEvent.
    """
    conf = events_conf()
    converter = _get_to_cloudevent_converter(event_name, conf)
    return converter(message)
