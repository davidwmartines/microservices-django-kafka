from dataclasses import dataclass
from datetime import datetime
from typing import Callable, NamedTuple
from uuid import UUID, uuid4

from django.conf import settings
from django.utils import timezone


class Config(NamedTuple):
    """
    Defines the configuration properties for creating events
    from model instances.
    """

    schema: str
    """
    Name of the schema to use.
    """

    topic: str
    """
    The topic name (subject) the schema will be registred to.
    """

    event_type: str
    """
    The type of event to generate.
    """

    to_dict: Callable[[object], dict]
    """
    Function that takes a model and returns a dictionary
    matching the data payload of the target schema.
    """


@dataclass
class Event:
    """
    A event occurrence to be produced or consumed from to Kafka,
    in the form of an event envelope structure containing
    the event data.
    This maps to a CloudEvents spec compliant event.
    """

    id: UUID
    source: str
    event_type: str
    time: datetime
    data: dict
    specversion: str = "1.0"


def create_event(event_type: str, data: dict) -> Event:
    """
    Utility function for creating an Event to be produced.
    """
    return Event(
        id=uuid4(),
        source=settings.EVENTS_SOURCE_NAME,
        event_type=event_type,
        time=timezone.now(),
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
