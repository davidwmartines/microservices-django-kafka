import os

from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import MessageField, SerializationContext
from django.conf import settings


class EventSerializer:
    """
    Serializes `Event` data.

    Callable.

    Arguments:
        schema (str): name of the schema to use for serializing events.

        topic (str): the target topic to which the schema will be registered to.

    """

    __slots__ = ["_schema", "_topic", "_serializer"]

    def __init__(self, schema: str, topic: str) -> None:
        self._schema = schema
        self._topic = topic

        # load the schema string from the referenced schema file
        with open(
            os.path.join(settings.BASE_DIR, settings.EVENTS_SCHEMAS_DIR, self._schema)
        ) as f:
            schema_string = f.read()

        # create schema registry client and avro serializer
        registry_client = SchemaRegistryClient({"url": settings.SCHEMA_REGISTRY_URL})
        self._serializer = AvroSerializer(registry_client, schema_string)

    def __call__(self, data: dict) -> str or bytes:
        return self._serializer(
            data, SerializationContext(self._topic, MessageField.VALUE)
        )
