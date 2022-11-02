import logging
from uuid import UUID

from events import Event, parse_date
from events.handlers import EventHandler

from planning.models import BalanceSheet, Person

logger = logging.getLogger(__name__)


class PersonEventHandler(EventHandler):

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
