import logging
from datetime import datetime

from cloudevents.abstract import AnyCloudEvent
from planning.models import BalanceSheet, Person

from events.handlers import CloudEventHandler

logger = logging.getLogger(__name__)


class PersonEventHandler(CloudEventHandler):
    """
    Handles Person events from Kafka
    by upserting a record into this service's local database.

    The incoming events are deserialized using the canonical Person
    schema defined in the specified avsc file.
    """

    def __init__(self) -> None:
        super().__init__(event_name="person_entity_state")

    def handle(self, event: AnyCloudEvent) -> None:

        data = event.data

        obj, created = Person.objects.update_or_create(
            id=data["id"],
            defaults={
                "date_of_birth": data["date_of_birth"]
                if "date_of_birth" in data
                else None,
            },
        )
        logger.info(f"persisted record for person {obj.id}. created: {created}")


class BalanceSheetEventHandler(CloudEventHandler):
    """
    Handles BalanceSheet events from Kafka
    by creating a balance sheet record in this service's local database.
    """

    def __init__(self) -> None:
        super().__init__(event_name="balance_sheet_created")

    def handle(self, event: AnyCloudEvent) -> None:
        data = event.data

        person_id = data["person_id"]

        if not Person.objects.filter(pk=person_id).exists():
            raise Exception(f"unknown person {person_id}")

        # logically, this would be saving a new balance sheet since they are
        # immutable instances.  However, using update_or_create to safely handle
        # duplicate events.
        obj, created = BalanceSheet.objects.update_or_create(
            id=data["id"],
            defaults={
                "person_id": person_id,
                "date_calculated": datetime.fromtimestamp(data["date_calculated"]),
                "assets": data["assets"],
                "liabilities": data["liabilities"],
            },
        )
        logger.info(
            f"persisted balance sheet {obj.id} for person {person_id}. created: {created}"
        )
