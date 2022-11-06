from events.handlers import EventHandler
from events.serializers import EventSerializer
from events.models import OutboxItem
from events import Event, parse_date
from uuid import uuid4

from django.conf import settings


class BalanceSheetCDCSchemaConverter(EventHandler):
    """
    This event handler consumes the balance-sheet events
    from the private topic created by the change-data-capture
    connector, and converts them to the canonical BalanceSheet event
    schema, and sends to the public topic.
    """

    target_topic = "public_balance_sheet_entity_events"
    target_schema = "balance_sheet.avsc"

    def __init__(self) -> None:
        super().__init__()
        self._reserializer = EventSerializer(
            schema=self.target_schema, topic=self.target_topic
        )

    def handle(self, event: Event) -> None:

        # create a new event in the canonical schema, based on the incoming data
        new_event = Event(
            id=uuid4(),
            source=settings.EVENTS_SOURCE_NAME,
            event_type="balance_sheet_created",
            time=parse_date(event["date_calculated"]),
            data=dict(
                id=event["id"],
                date_calculated=event["date_calculated"],
                person_id=event["person_id"],
                assets=event["assets"],
                liabilities=event["liabilities"],
            ),
        )

        # save it to the outbox
        outbox_item = OutboxItem.from_event(
            new_event,
            topic=self.target_topic,
            key=event["id"],
            serializer=self._reserializer,
        )
        outbox_item.save()
