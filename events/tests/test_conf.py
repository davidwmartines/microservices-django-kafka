from django.test import TestCase
from events.conf import EventsConfiguration, EventType, events_conf
from events.enums import CloudEventsMode, SerializationFormat


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
                "DEFAULTS": {"FORMAT": "json", "MODE": "structured"},
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
                conf.types["an.event.type"].format, SerializationFormat.JSON
            )
            self.assertEqual(
                conf.types["an.event.type"].mode, CloudEventsMode.STRUCTURED
            )

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
                events_conf()

    def test_raises_key_error_when_name_not_specified(self):
        with self.settings(
            EVENTS={
                "TYPES": [
                    {
                        "TOPIC": "my-topic",
                        "SCHEMA": "schema.avsc",
                    },
                ],
                "DEFAULTS": {"FORMAT": "avro", "MODE": "binary"},
                "SCHEMA_REGISTRY_URL": "http://schema-registry:8081",
                "EVENT_SOURCE_NAME": "my-app",
            }
        ):

            with self.assertRaises(KeyError):
                events_conf()

    def test_raises_key_error_when_topic_not_specified(self):
        with self.settings(
            EVENTS={
                "TYPES": [
                    {
                        "NAME": "an.event.type",
                        "SCHEMA": "schema.avsc",
                    },
                ],
                "DEFAULTS": {"FORMAT": "avro", "MODE": "binary"},
                "SCHEMA_REGISTRY_URL": "http://schema-registry:8081",
                "EVENT_SOURCE_NAME": "my-app",
            }
        ):

            with self.assertRaises(KeyError):
                events_conf()

    def test_applies_built_in_defaults(self):
        with self.settings(
            EVENTS={
                "TYPES": [
                    {
                        "NAME": "an.event.type",
                        "SCHEMA": "schema.avsc",
                        "TOPIC": "my-topic",
                    },
                ],
                "DEFAULTS": {},
                "SCHEMA_REGISTRY_URL": "http://schema-registry:8081",
                "EVENT_SOURCE_NAME": "my-app",
            }
        ):
            conf = events_conf()
            self.assertEqual(
                conf.types["an.event.type"].format, SerializationFormat.AVRO
            )
            self.assertEqual(conf.types["an.event.type"].mode, CloudEventsMode.BINARY)

    def test_multipe_types(self):
        with self.settings(
            EVENTS={
                "TYPES": [
                    {
                        "NAME": "an.event.type",
                        "SCHEMA": "schema.avsc",
                        "TOPIC": "my-topic",
                    },
                    {
                        "NAME": "com.github.pullrequest.opened",
                        "SCHEMA": "pull_request.avsc",
                        "TOPIC": "pull_requests",
                        "FORMAT": "json",
                        "MODE": "structured",
                    },
                ],
                "DEFAULTS": {"FORMAT": "avro", "MODE": "binary"},
                "SCHEMA_REGISTRY_URL": "http://schema-registry:8081",
                "EVENT_SOURCE_NAME": "my-app",
            }
        ):
            conf = events_conf()
            self.assertEqual(2, len(conf.types))

            type_1 = conf.types["an.event.type"]
            self.assertEqual(type_1.name, "an.event.type")
            self.assertEqual(type_1.schema, "schema.avsc")
            self.assertEqual(type_1.topic, "my-topic")
            self.assertEqual(type_1.format, SerializationFormat.AVRO)
            self.assertEqual(type_1.mode, CloudEventsMode.BINARY)

            type_2 = conf.types["com.github.pullrequest.opened"]
            self.assertEqual(type_2.name, "com.github.pullrequest.opened")
            self.assertEqual(type_2.schema, "pull_request.avsc")
            self.assertEqual(type_2.topic, "pull_requests")
            self.assertEqual(type_2.format, SerializationFormat.JSON)
            self.assertEqual(type_2.mode, CloudEventsMode.STRUCTURED)
