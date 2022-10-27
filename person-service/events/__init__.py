from dataclasses import dataclass
from datetime import datetime
from typing import Callable, NamedTuple
from uuid import UUID, uuid4

from django.conf import settings
from django.utils import timezone


class Config(NamedTuple):
    """
    Defines the configuration properties for creating events.
    """

    schema: str
    """
    Name of the schema to use.
    """

    topic: str
    """
    The topic name (subject) the schema will be registred to.
    """

    to_dict: Callable[[object], dict]
    """
    function that takes a model and returns a dictionary
    matching the data payload of the target schema.
    """


@dataclass
class EventEnvelope:
    id: UUID
    source: str
    event_type: str
    time: datetime
    data: dict
    specversion: str = "1.0"


def create_event(event_type: str, data: dict) -> EventEnvelope:
    return EventEnvelope(
        id=uuid4(),
        source=settings.EVENT_SOURCE_NAME,
        event_type="entity.saved",
        time=timezone.now(),
        data=data,
    )
