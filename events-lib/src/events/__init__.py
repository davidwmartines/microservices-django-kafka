from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from django.conf import settings


@dataclass
class Event:
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


def dict_to_event(val: dict, *args) -> Event:
    """
    Utility function for converting a deserialized
    dict from an incoming message into an Event.
    """
    return Event(
        UUID(val["id"]),
        val["source"],
        val["type"],
        parse_date(val["time"]),
        val["data"],
        val["specversion"],
    )
