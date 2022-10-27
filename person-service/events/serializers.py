from typing import Any
from confluent_kafka.serialization import (
    SerializationContext,
    MessageField,
)
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
import os

from django.conf import settings
from . import Config, EventEnvelope


class EventSerializer:
    def __init__(self, config: Config) -> None:
        self.config = config

        # load the schema string from the referenced schema file
        path = os.path.realpath(os.path.dirname(__file__))
        with open(f"{path}/schemas/{config.schema}") as f:
            schema_string = f.read()

        # create schema registry client and avro serializer
        registry_client = SchemaRegistryClient({"url": settings.SCHEMA_REGISTRY_URL})
        self.avro_serializer = AvroSerializer(
            registry_client,
            schema_string,
            to_dict=lambda event, ctx: dict(
                id=str(event.id),
                type=event.event_type,
                source=event.source,
                specversion=event.specversion,
                time=event.time.isoformat(),
                data=event.data,
            ),
        )

    def __call__(self, event: EventEnvelope) -> Any:
        return self.avro_serializer(
            event, SerializationContext(self.config.topic, MessageField.VALUE)
        )
