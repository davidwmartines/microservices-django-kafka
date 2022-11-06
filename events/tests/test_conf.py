from django.test import TestCase, override_settings

from src.events.conf import events_conf, EventsConfiguration, EventType


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
