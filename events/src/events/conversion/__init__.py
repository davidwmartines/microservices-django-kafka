from .. import Event
from dataclasses import dataclass


@dataclass
class ProtocolEvent:
    event: Event
    body: bytes


class EventConverter:
    def __call__(self, event: Event, *args, **kwargs) -> ProtocolEvent:
        raise NotImplementedError()


class ProtocolEventConverter:
    def __call__(self, event: ProtocolEvent, *args, **kwargs) -> Event:
        raise NotImplementedError()
