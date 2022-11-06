from django.conf import settings
from typing import NamedTuple

import sys

this = sys.modules[__name__]


class EventsConfiguration(NamedTuple):

    types: dict = {}
    defaults: dict = {}
    schema_registry_url: str = ""
    bootstrap_servers: str = ""
    event_source_name: str = ""


class EventType(NamedTuple):
    name: str
    schema: str
    topic: str
    format: str
    mode: str


this.conf_instance: EventsConfiguration = None


def events_conf() -> EventsConfiguration:
    if this.conf_instance:
        return this.conf_instance

    conf_section = getattr(settings, "EVENTS")
    if not conf_section:
        raise ValueError("EVENTS not configured in settings")

    defaults = conf_section.get("DEFAULTS", {})
    this.conf_instance = EventsConfiguration(
        types={
            t["NAME"]: EventType(
                t["NAME"],
                t["SCHEMA"],
                t["TOPIC"],
                t.get("FORMAT", defaults.get("FORMAT", "AVRO")),
                t.get("MODE", defaults.get("MODE", "BINARY")),
            )
            for t in conf_section.get("TYPES", [])
        },
        schema_registry_url=str(conf_section["SCHEMA_REGISTRY_URL"]),
        bootstrap_servers=str(conf_section.get("BOOTSTRAP_SERVERS", "")),
        event_source_name=conf_section["EVENT_SOURCE_NAME"],
    )

    return this.conf_instance
