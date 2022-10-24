from django.db import models
from django_extensions.db.models import TimeStampedModel
from datetime import datetime


def demo_date_of_birth():
    return datetime(1970, 1)


class Person(TimeStampedModel):
    id = models.UUIDField(primary_key=True)
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    date_of_birth = models.DateTimeField(
        null=True, blank=True, default=demo_date_of_birth
    )

    def __str__(self):
        return f"{self.last_name}, {self.first_name} | {self.id}"
