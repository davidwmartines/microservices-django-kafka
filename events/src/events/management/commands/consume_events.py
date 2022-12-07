import logging

import djclick as click
from confluent_kafka import Consumer
from django.utils.module_loading import import_string

from ...conf import events_conf

logger = logging.getLogger(__name__)


@click.command()
@click.option("--topic")
@click.option("--consumer_group_id")
@click.option("--handler")
@click.option("--allow_errors", is_flag=True, default=False)
@click.option("--initial_offset", default=0)
def command(topic, consumer_group_id, handler, allow_errors, initial_offset):
    logger.info("Starting consumer")

    conf = events_conf()
    if not conf.bootstrap_servers:
        raise ValueError("EVENTS.BOOTSTRAP_SERVERS not configured in settings.")

    auto_commit = False

    if allow_errors:
        logger.warning(
            """RUNNING IN ALLOW_ERRORS MODE!  Not all events are guaranteed to be
            handled succesfully, but offsets will be comitted.  Any handler errors
            will be logged."""
        )
        auto_commit = True

    handler_class = import_string(handler)
    logger.info(f"imported handler {handler}")

    handler_instance = handler_class()
    logger.debug(f"instantiated handler {handler}")

    consumer = Consumer(
        {
            "bootstrap.servers": conf.bootstrap_servers,
            "group.id": consumer_group_id,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": auto_commit,
        }
    )

    logger.info(f"subscribing to topic {topic}")
    consumer.subscribe([topic])

    if initial_offset:
        logger.info(f"Seeking to offset {initial_offset}")

        # poll once to get assigments
        consumer.poll(1.0)

        # seek to the specified offset:
        # TODO: seek based on partition:offset
        for topic_partition in consumer.assignment():
            topic_partition.offset = initial_offset
            consumer.seek(topic_partition)

    logger.info(f"starting consume loop")
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue

        if msg.error():
            logger.warn(msg.error())
            continue
        else:
            logger.debug("dispatching message to handler")
            try:
                handler_instance(msg)
            except Exception as ex:
                logger.error(
                    f"""Exception handling message from partition {msg.partition()},
                    offset: {msg.offset()}.  Headers: {msg.headers()} {str(ex)}""",
                    exc_info=str(ex),
                )
                if not allow_errors:
                    raise ex

            if not auto_commit:
                consumer.commit(msg)
                logger.debug(f"Committed message at offset {msg.offset()}")
