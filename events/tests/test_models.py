from datetime import datetime, timezone

import responses
from django.test import TestCase
from src.events import create_event
from src.events.models import OutboxItem
from src.events.conversion.kafka import BinaryKafkaEventConverter


class OutboxItemTestCase(TestCase):
    def test_create_from_event(self):

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

            item = OutboxItem.from_event(event, key="12345")

            self.assertEqual(item.id, event.id)
            self.assertEqual(item.content_type, "application/avro")
            self.assertEqual(item.event_type, "com.github.pullrequest.opened")
            self.assertEqual(item.message_key, "12345")
            self.assertEqual(item.source, "my-app")
            self.assertEqual(item.topic, "pull_requests")
            self.assertEqual(item.timestamp, event.time)
            self.assertIsInstance(item.payload, bytes)
