from . import Event
from . import EventConverter
from ..conf import events_conf
from ..enums import CloudEventsMode
from .kafka import BinaryKafkaEventConverter


def get_converter(event: Event) -> EventConverter:
    """
    Factory function for getting the correct converter for the type of event
    """

    conf = events_conf()
    type_conf = conf.types.get(event.type)
    if not type_conf:
        raise KeyError(f"{event.type} is not configured in settings.")

    if type_conf.mode == CloudEventsMode.BINARY:
        # this is the only converted implemented now
        return BinaryKafkaEventConverter()

    raise NotImplementedError()
