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
        topic="public_person_entity_events",
        event_type="person_entity_state",
        to_dict=lambda o: dict(
            id=str(o.id),
            first_name=o.first_name,
            last_name=o.last_name,
            date_of_birth=o.date_of_birth.isoformat(),
        ),
    )
)
class Person(TimeStampedModel):
    """
    Represents a human known to the Person Service.
    The Person Service is considered the authoritative
    system of record for Person data in the microservices
    ecosystem.
    """
    id = models.UUIDField(primary_key=True, default=uuid4)
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    date_of_birth = models.DateTimeField(
        null=True, blank=True, default=demo_date_of_birth
    )
