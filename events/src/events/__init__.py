from datetime import datetime, timezone
from typing import NamedTuple
from uuid import UUID, uuid4


class Event(NamedTuple):
    """
    An event occurrence to be produced or consumed from to Kafka,
    in the form of an event envelope structure containing
    the event data.
    This maps to a CloudEvents spec event.
    """

    id: UUID
    type: str
    time: datetime
    data: dict or object
    source: str = ""


def create_event(type: str, data: dict) -> Event:
    """
    Utility function for creating an Event to be produced.
    """
    return Event(
        id=uuid4(),
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
