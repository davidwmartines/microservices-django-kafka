from uuid import UUID
import dateutil.parser

from events import create_event
from events.handlers import GenericEventHandler
from events.models import OutboxItem


class OrderCDCSchemaConverter(GenericEventHandler):
    """
    This event handler consumes the order events
    from the private topic created by the change-data-capture
    connector, and converts them to the canonical Order event
    schema, and sends to the public topic.
    """

    def __init__(self) -> None:
        super().__init__()

    def handle(self, data: dict, headers: dict) -> None:
        # Create a CloudEvent from the incoming message data.
        # In this case the fields are identically named, but typically
        # the target event type would have a different schema
        # than the source table.
        # Note the type conversions needed.
        event = create_event(
            "order_created",
            data=dict(
                id=UUID(data["id"]),
                date_placed=dateutil.parser.isoparse(data["date_placed"]),
                customer_id=UUID(data["customer_id"]),
                item_count=int(data["item_count"]),
            ),
            key=data["id"],
        )

        # save it to the outbox
        outbox_item = OutboxItem.from_event(event)
        outbox_item.save()
