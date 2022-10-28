from datetime import datetime
from uuid import UUID

from events import Event
from events.handlers import EventHandler

from planning.models import Person

import logging

logger = logging.getLogger(__name__)


class PersonEventHandler(EventHandler):
    def schema_file_name(self) -> str:
        return "person.avsc"

    def handle(self, event: Event) -> None:

        data = event.data

        obj, created = Person.objects.update_or_create(
            id=UUID(data["id"]),
            defaults={
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "date_of_birth": datetime.fromisoformat(data["date_of_birth"])
                if "date_of_birth" in data
                else None,
            },
        )
        logger.info(f"persisted record for person {obj.id}. created: {created}")
