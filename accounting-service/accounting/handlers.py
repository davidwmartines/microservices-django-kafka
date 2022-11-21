from uuid import UUID

from events import create_event, parse_date
from events.handlers import GenericEventHandler
from events.models import OutboxItem


class BalanceSheetCDCSchemaConverter(GenericEventHandler):
    """
    This event handler consumes the balance-sheet events
    from the private topic created by the change-data-capture
    connector, and converts them to the canonical BalanceSheet event
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
            "balance_sheet_created",
            data=dict(
                id=UUID(data["id"]),
                date_calculated=parse_date(data["date_calculated"]),
                person_id=UUID(data["person_id"]),
                assets=int(data["assets"]),
                liabilities=int(data["liabilities"]),
            ),
            key=data["id"],
        )

        # save it to the outbox
        outbox_item = OutboxItem.from_event(event)
        outbox_item.save()
