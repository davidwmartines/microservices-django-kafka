import djclick as click
import logging


from confluent_kafka import Consumer
from django.utils.module_loading import import_string

from django.conf import settings

logger = logging.getLogger(__name__)


@click.command()
@click.option("--topic")
@click.option("--consumer_group_id")
@click.option("--handler")
def command(topic, consumer_group_id, handler):

    logger.info("Starting consumer")

    handler_func = import_string(handler)()
    logger.info(f"imported handler {handler}")

    consumer = Consumer(
        {
            "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
            "group.id": consumer_group_id,
            "auto.offset.reset": "earliest",
        }
    )
    logger.info(f"subscribing to topic {topic}")
    consumer.subscribe([topic])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue

        if msg.error():
            logger.warn(msg.error())
            continue
        else:
            logger.debug("dispatching message to handler")
            handler_func(msg)
