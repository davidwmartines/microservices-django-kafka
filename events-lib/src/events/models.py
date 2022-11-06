from django.db import models
from events import Event
from typing import Callable


class OutboxItem(models.Model):
    """
    Stores a serialized event and metadata to the outbox table.
    The event will be produced to Kafka by a relaying process -
    i.e. Kafka-Connect via the Debezium Outbox Event Router.
    """

    id = models.UUIDField(primary_key=True)
    """
    The unique id of the event. This should match the event payload id field.
    """

    topic = models.CharField(max_length=255, null=False)
    """
    Value passed to the Debezium Outbox Event Router for routing to a specific topic.
    Typically based on the name of the entity class related to the event occurrence.
    """

    message_key = models.CharField(max_length=255, null=False)
    """
    Value passed to the Debezium Outbox Event Router to set the KEY on
    messages to Kafka.
    This should almost always be the ID of the entity instance related the event occurrence.
    """

    timestamp = models.DateTimeField(null=False)
    "Timestamp of the event occurrence."

    event_type = models.CharField(max_length=255, null=False)
    """
    The type of event related to the event occurrence.
    """

    source = models.CharField(max_length=255, null=False, default="")
    """
    Source URI of the occurrence.
    """

    content_type = models.CharField(
        max_length=255, null=False, default="application/avro"
    )
    """
    Value for the content-type header.
    """

    payload = models.BinaryField()
    """
    The Avro-Serialized message containing the entire event payload
    (envelope and data).
    """

    @classmethod
    def from_event(
        cls,
        event: Event,
        topic: str,
        key: str,
        serializer: Callable[[dict], str or bytes],
    ):
        """
        Utility function for creating an OutboxItem from an event instance.
        """

        payload = serializer(event.data)

        return OutboxItem(
            id=event.id,
            topic=topic,
            message_key=key,
            timestamp=event.time,
            event_type=event.type,
            source=event.source,
            content_type="application/avro",
            payload=payload,
        )
