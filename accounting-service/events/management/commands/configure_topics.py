import logging

import djclick as click
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
from django.conf import settings
import os

logger = logging.getLogger(__name__)

DEFAULT_PARTITION_COUNT = 8
DEFAULT_REPLICACTION_FACTOR = 1


@click.command()
def command():
    """
    This command can be used to pre-create topics and register schemas,
    in cases where this is needed.
    """

    topic_configs = settings.KAFKA_TOPIC_CONFIGS

    _create_topics(topic_configs)

    _register_schemas(topic_configs)


def _create_topics(configs: dict) -> None:
    new_topics = [
        NewTopic(
            config["name"],
            num_partitions=config.get("partitions", DEFAULT_PARTITION_COUNT),
            replication_factor=config.get(
                "replication_factor", DEFAULT_REPLICACTION_FACTOR
            ),
        )
        for config in configs
    ]
    admin_client = AdminClient({"bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS})
    fs = admin_client.create_topics(new_topics)
    for topic, f in fs.items():
        try:
            f.result()
            logger.info("Topic {} created".format(topic))
        except Exception as e:
            logger.warn("Did not create topic {}: {}".format(topic, e))


def _register_schemas(configs: dict) -> None:

    schema_registry_client = SchemaRegistryClient({"url": settings.SCHEMA_REGISTRY_URL})

    for config in configs:
        schema_file_name = config["schema"]
        try:
            schema = _get_schema(schema_file_name)
            id = schema_registry_client.register_schema(
                subject_name=config["name"], schema=schema
            )
            logger.info(f"Registered schema {schema_file_name}, id {id}")
        except Exception as e:
            logger.warn("Did not register schema {}: {}".format(schema_file_name, e))


def _get_schema(file_name: str) -> Schema:
    with open(
        os.path.join(settings.BASE_DIR, settings.EVENTS_SCHEMAS_DIR, file_name)
    ) as f:
        schema_string = f.read()
    return Schema(schema_string, schema_type="AVRO")
