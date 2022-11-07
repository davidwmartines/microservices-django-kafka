from django.test import TestCase
from src.events.models import OutboxItem

from .testapp.models import Widget
import responses


# class SaveEventDecorator(TestCase):
#     def test_save_event(self):
#         with self.settings(
#             EVENTS={
#                 "TYPES": [
#                     {
#                         "NAME": "widget_event",
#                         "SCHEMA": "widget.avsc",
#                         "TOPIC": "widgets",
#                     },
#                 ],
#                 "DEFAULTS": {"FORMAT": "avro", "MODE": "binary"},
#                 "SCHEMA_REGISTRY_URL": "http://schema-registry:8081",
#                 "EVENT_SOURCE_NAME": "my-app",
#                 "SCHEMAS_DIR": "tests/schemas",
#             },
#             USE_TZ=True
#         ), responses.RequestsMock(assert_all_requests_are_fired=False) as resp:

#             resp.add(
#                 resp.POST,
#                 "http://schema-registry:8081/subjects/widgets-value/versions",
#                 json={"id": 123},
#                 status=200,
#             )
#             widget = Widget(name="A Test Widget")

#             widget.save()
