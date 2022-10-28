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


def dict_to_event(val: dict, *args) -> Event:
    return Event(
        UUID(val["id"]),
        val["source"],
        val["type"],
        datetime.fromisoformat(val["time"]),
        val["data"],
        val["specversion"],
    )
