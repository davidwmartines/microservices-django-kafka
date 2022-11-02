import logging
from uuid import UUID

from events import Event, parse_date
from events.handlers import EventHandler

from planning.models import BalanceSheet, Person

logger = logging.getLogger(__name__)


class PersonEventHandler(EventHandler):
    """
    Handles Person events from Kafka
    by upserting a record into this service's local database.

    The incoming events are deserialized using the canonical Person
    schema defined in the specified avsc file.
    """

    schema_file_name = "person.avsc"

    def handle(self, event: Event) -> None:

        data = event.data

        obj, created = Person.objects.update_or_create(
            id=UUID(data["id"]),
            defaults={
                "date_of_birth": parse_date(data["date_of_birth"])
                if "date_of_birth" in data
                else None,
            },
        )
        logger.info(f"persisted record for person {obj.id}. created: {created}")


class BalanceSheetEventHandler(EventHandler):
    """
    Handles BalanceSheet events from Kafka
    by creating a balance sheet record in this service's local database.

    Note:  For this handler, we do not specify a reader-schema file.
    This is because these events are actually serialized by ksqlb using its
    own logical schema, which does not match the canonical BalanceSheet schema,
    even though it is functionally identical.  The data we receive matches
    the expected structure.

    TODO: Make the selection of schema file not so reliant on knowing what schema
    the source system is using (either canonical avsc file or ksql-generated).
    """

    def handle(self, event: Event) -> None:
        data = event.data

        person_id = UUID(data["person_id"])

        if not Person.objects.filter(pk=person_id).exists():
            raise Exception(f"unknown person {person_id}")

        # logically, this would be saving a new balance sheet since they are
        # immutable instances.  However, using update_or_create to safely handle
        # duplicate events.
        obj, created = BalanceSheet.objects.update_or_create(
            id=UUID(data["id"]),
            defaults={
                "person_id": person_id,
                "date_calculated": parse_date(data["date_calculated"]),
                "assets": int(data["assets"]),
                "liabilities": int(data["liabilities"]),
            },
        )
        logger.info(
            f"persisted balance sheet {obj.id} for person {person_id}. created: {created}"
        )
