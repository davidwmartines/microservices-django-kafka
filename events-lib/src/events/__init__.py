from datetime import datetime, timezone
from typing import NamedTuple, Callable
from uuid import UUID, uuid4

from django.conf import settings


class Event(NamedTuple):
    """
    An event occurrence to be produced or consumed from to Kafka,
    in the form of an event envelope structure containing
    the event data.
    This maps to a CloudEvents spec event.
    """

    id: UUID
    source: str
    type: str
    time: datetime
    data: dict
    specversion: str = "1.0"


def create_event(type: str, data: dict) -> Event:
    """
    Utility function for creating an Event to be produced.
    """
    return Event(
        id=uuid4(),
        source=settings.EVENTS_SOURCE_NAME,
        type=type,
        time=datetime.now(timezone.utc),
        data=data,
    )


def parse_date(val: str) -> datetime:
    """
    Handle different variations of datetime as a string.
    Python serialized datetimes are isoformatted.
    KSQL serialized have the Z at the end.
    """
    return datetime.fromisoformat(str(val).replace("Z", "+00:00"))


class BinaryModeEvent(NamedTuple):
    """
    Represents an event in binary mode representation.
    """

    headers: dict
    data: bytes


def to_binary(
    event: Event, data_serializer: Callable[[Event], str or bytes]
) -> BinaryModeEvent:
    return BinaryModeEvent(
        headers={
            "ce_id": str(event.id),
            "ce_type": event.type,
            "ce_source": event.source,
            "ce_time": event.time.isoformat(),
            "content-type": "application/avro",
        },
        data=data_serializer(event.data),
    )


def from_binary(
    headers: dict, data: str or bytes, data_deserializer: Callable[[str or bytes], dict]
) -> Event:
    return Event(
        id=UUID(headers["ce_id"]),
        type=headers["ce_type"],
        source=headers["ce_source"],
        time=parse_date(headers["ce_time"]),
        data=data_deserializer(data),
    )
