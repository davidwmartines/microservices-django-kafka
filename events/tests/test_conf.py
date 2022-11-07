from django.test import TestCase
from src.events.conf import EventsConfiguration, EventType, events_conf

from src.events.enums import CloudEventsMode, SerializationFormat


class EventsConfTestCase(TestCase):
    def test_loads_minimal_required_conf(self):
        with self.settings(
            EVENTS={
                "SCHEMA_REGISTRY_URL": "http://schema-registry:8081",
                "EVENT_SOURCE_NAME": "my-app",
            }
        ):
            conf = events_conf()

            self.assertIsInstance(conf, EventsConfiguration)

            self.assertEqual(conf.schema_registry_url, "http://schema-registry:8081")
            self.assertEqual(conf.event_source_name, "my-app")
            self.assertEqual(conf.bootstrap_servers, "")
            self.assertDictEqual({}, conf.types)

    def test_loads_event_type_setting(self):
        with self.settings(
            EVENTS={
                "TYPES": [
                    {
                        "NAME": "an.event.type",
                        "SCHEMA": "schema.avsc",
                        "TOPIC": "my-topic",
                        "FORMAT": "avro",
                        "MODE": "binary",
                    },
                ],
                "SCHEMA_REGISTRY_URL": "http://schema-registry:8081",
                "EVENT_SOURCE_NAME": "my-app",
            }
        ):
            conf = events_conf()
            self.assertEqual(1, len(conf.types))
            self.assertTrue("an.event.type" in conf.types)
            self.assertIsInstance(conf.types["an.event.type"], EventType)
            self.assertEqual(conf.types["an.event.type"].name, "an.event.type")
            self.assertEqual(conf.types["an.event.type"].schema, "schema.avsc")
            self.assertEqual(conf.types["an.event.type"].topic, "my-topic")
            self.assertEqual(
                conf.types["an.event.type"].format, SerializationFormat.AVRO
            )
            self.assertEqual(conf.types["an.event.type"].mode, CloudEventsMode.BINARY)

    def test_loads_event_type_with_defaults(self):
        with self.settings(
            EVENTS={
                "TYPES": [
                    {
                        "NAME": "an.event.type",
                        "SCHEMA": "schema.avsc",
                        "TOPIC": "my-topic",
                    },
                ],
                "DEFAULTS": {"FORMAT": "avro", "MODE": "binary"},
                "SCHEMA_REGISTRY_URL": "http://schema-registry:8081",
                "EVENT_SOURCE_NAME": "my-app",
            }
        ):

            conf = events_conf()
            self.assertEqual(1, len(conf.types))
            self.assertTrue("an.event.type" in conf.types)
            self.assertIsInstance(conf.types["an.event.type"], EventType)
            self.assertEqual(conf.types["an.event.type"].name, "an.event.type")
            self.assertEqual(conf.types["an.event.type"].schema, "schema.avsc")
            self.assertEqual(conf.types["an.event.type"].topic, "my-topic")
            self.assertEqual(
                conf.types["an.event.type"].format, SerializationFormat.AVRO
            )
            self.assertEqual(conf.types["an.event.type"].mode, CloudEventsMode.BINARY)

    def test_raises_key_error_when_schema_not_specified(self):
        with self.settings(
            EVENTS={
                "TYPES": [
                    {
                        "NAME": "an.event.type",
                        "TOPIC": "my-topic",
                    },
                ],
                "DEFAULTS": {"FORMAT": "avro", "MODE": "binary"},
                "SCHEMA_REGISTRY_URL": "http://schema-registry:8081",
                "EVENT_SOURCE_NAME": "my-app",
            }
        ):

            with self.assertRaises(KeyError):
                conf = events_conf()
