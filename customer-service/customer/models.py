from django.db import models
from django_extensions.db.models import TimeStampedModel
from datetime import datetime
from uuid import uuid4
from events.decorators import save_event, Config


@save_event(
    Config(
        type="customer_entity_state",
        to_dict=lambda o: dict(
            id=o.id,
            first_name=o.first_name,
            last_name=o.last_name,
            date_established=o.date_established,
        ),
    )
)
class Customer(TimeStampedModel):
    """
    Represents a Customer.
    The Customer Service is considered the authoritative
    system of record for Customer data in the microservices
    ecosystem.
    """

    id = models.UUIDField(primary_key=True, default=uuid4)
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    date_established = models.DateTimeField(null=True, blank=True, default=datetime.now)
