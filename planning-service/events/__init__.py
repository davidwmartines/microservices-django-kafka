from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Event:
    """
    Represents a CloudEvents spec compliant event envelope.
    """

    id: UUID
    source: str
    event_type: str
    time: datetime
    data: dict
    specversion: str = "1.0"


def parse_date(val: str) -> datetime:
    """
    Handle different variations of datetime as a string.
    Python serialized datetimes are isoformatted.
    KSQL serialized have the Z at the end.
    """
    return datetime.fromisoformat(str(val).replace("Z", ""))


def dict_to_event(val: dict, *args) -> Event:
    return Event(
        UUID(val["id"]),
        val["source"],
        val["type"],
        parse_date(val["time"]),
        val["data"],
        val["specversion"],
    )
