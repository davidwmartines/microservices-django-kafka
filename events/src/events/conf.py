import sys
from typing import NamedTuple, Callable
import os

from django.conf import settings
from django.core.signals import setting_changed
from django.test.signals import setting_changed as setting_changed_test

from django.db.models import Model

from .enums import CloudEventsMode, SerializationFormat

from . import Event


class EventsConfiguration(NamedTuple):
    types: dict = {}
    defaults: dict = {}
    schema_registry_url: str = ""
    bootstrap_servers: str = ""
    event_source_name: str = ""
    schemas_dir: str = ""


class EventType(NamedTuple):
    name: str
    schema: str
    topic: str
    format: str
    mode: str


# singleton instance
this = sys.modules[__name__]
this.conf_instance: EventsConfiguration = None


def events_conf() -> EventsConfiguration:
    """
    Gets the EventConfiguration.
    """
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
                SerializationFormat(t.get("FORMAT", defaults.get("FORMAT", "avro"))),
                CloudEventsMode(t.get("MODE", defaults.get("MODE", "binary"))),
            )
            for t in conf_section.get("TYPES", [])
        },
        schema_registry_url=str(conf_section["SCHEMA_REGISTRY_URL"]),
        bootstrap_servers=str(conf_section.get("BOOTSTRAP_SERVERS", "")),
        event_source_name=conf_section["EVENT_SOURCE_NAME"],
        schemas_dir=os.path.join(
            settings.BASE_DIR, conf_section.get("SCHEMAS_DIR", "schemas")
        )
    )

    return this.conf_instance


def on_settings_changed(sender, **kwargs):
    this.conf_instance = None


setting_changed.connect(on_settings_changed)
setting_changed_test.connect(on_settings_changed)



