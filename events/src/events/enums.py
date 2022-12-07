from enum import Enum


class CloudEventsMode(str, Enum):
    """
    Enumerates the content modes for Cloud Events.
    """

    BINARY = "binary"
    """
    The event data is passed as the body or value, and the cloud events envelope fields
    are passed as headers.
    """

    STRUCTURED = "structured"
    """
    The body of the message specfies both the cloud events envelope fields and the event
    data as the `data` field.
    """


class SerializationFormat(str, Enum):
    """
    Supported Serialization Formats.
    """

    AVRO = "avro"
    JSON = "json"
