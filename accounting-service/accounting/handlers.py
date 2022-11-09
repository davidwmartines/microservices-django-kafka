from events.handlers import GenericEventHandler
from events import create_event
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
        # In this case the fields are identical, but typically
        # the target event type would have a different schema
        # than the source table.
        event = create_event(
            "balance_sheet_created",
            data=dict(
                id=data["id"],
                date_calculated=data["date_calculated"],
                person_id=data["person_id"],
                assets=data["assets"],
                liabilities=data["liabilities"],
            ),
            key=data["id"],
        )

        # save it to the outbox
        outbox_item = OutboxItem.from_event(event)
        outbox_item.save()
