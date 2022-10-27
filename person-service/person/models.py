from django.db import models
from django_extensions.db.models import TimeStampedModel
from datetime import datetime
from uuid import uuid4
from events.decorators import save_event
from events import Config


def demo_date_of_birth():
    return datetime(1970, 1, 1)


@save_event(
    Config(
        schema="person.avsc",
        topic="person_entity_events",
        to_dict=lambda o: dict(
            id=str(o.id),
            first_name=o.first_name,
            last_name=o.last_name,
            date_of_birth=o.date_of_birth.isoformat(),
        ),
    )
)
class Person(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4)
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    date_of_birth = models.DateTimeField(
        null=True, blank=True, default=demo_date_of_birth
    )

    def __str__(self):
        return f"{self.last_name}, {self.first_name} | {self.id}"
