from datetime import datetime

from cloudevents import http
from cloudevents.abstract import AnyCloudEvent

from .conf import events_conf


def create_event(
    type: str, data: dict or object, key: str or bytes = None
) -> AnyCloudEvent:
    """
    Utility function for creating a CloudEvent to be produced.
    """

    # id and time are automatically set by CloudEvent
    return http.CloudEvent.create(
        {
            "source": events_conf().event_source_name,
            "type": type,
            "partitionkey": key,
        },
        data,
    )


def parse_date(val: str) -> datetime:
    """
    Handle different variations of datetime as a string.
    Python serialized datetimes are isoformatted.
    KSQL serialized have the Z at the end.
    """
    return datetime.fromisoformat(str(val).replace("Z", "+00:00"))
