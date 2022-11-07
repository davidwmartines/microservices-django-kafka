from datetime import datetime, timezone

import responses
from django.test import TestCase
from events import create_event
from events.conversion.kafka import BinaryKafkaEventConverter


class BinaryKafkaEventConverterTestCase(TestCase):
    def test_call(self):

        with self.settings(
            EVENTS={
                "TYPES": [
                    {
                        "NAME": "com.github.pullrequest.opened",
                        "SCHEMA": "pull_request.avsc",
                        "TOPIC": "pull_requests",
                    },
                ],
                "DEFAULTS": {"FORMAT": "avro", "MODE": "binary"},
                "SCHEMA_REGISTRY_URL": "http://schema-registry:8081",
                "EVENT_SOURCE_NAME": "my-app",
                "SCHEMAS_DIR": "tests/schemas",
            }
        ), responses.RequestsMock(assert_all_requests_are_fired=False) as resp:

            resp.add(
                resp.POST,
                "http://schema-registry:8081/subjects/pull_requests-value/versions",
                json={"id": 123},
                status=200,
            )

            event = create_event(
                "com.github.pullrequest.opened",
                data={
                    "id": 12345,
                    "url": "https://github.com/org/repo/pull/12345",
                    "title": "bart's PR",
                    "author": "bartsimpson",
                    "opened_on": datetime(2000, 1, 1, tzinfo=timezone.utc).isoformat(),
                },
            )
            converter = BinaryKafkaEventConverter()
            protocol_event = converter(event, key_mapper=lambda e: str(12345))

            self.assertEqual(protocol_event.key, "12345")
            self.assertEqual(protocol_event.topic, "pull_requests")
            self.assertIsInstance(protocol_event.body, bytes)
            self.assertIsInstance(protocol_event.headers, dict)
            self.assertEqual(protocol_event.headers["ce_id"], str(event.id))
            self.assertEqual(protocol_event.headers["ce_source"], "my-app")
            self.assertEqual(protocol_event.headers["ce_time"], event.time.isoformat())
            self.assertEqual(protocol_event.headers["ce_type"], event.type)
            self.assertEqual(protocol_event.headers["ce_specversion"], "1.0")
            self.assertEqual(protocol_event.headers["content-type"], "application/avro")
