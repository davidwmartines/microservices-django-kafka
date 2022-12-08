from django.db import models
from datetime import date


class Person(models.Model):
    """
    Represents a human known to the Planning Service,
    and all the information about a person for the purpose
    of financial planning.
    Person data comes from the microservice ecosystem
    via the person entity state stream.  The person data
    in this service is not considered authoritative and
    is not managed here.
    """

    id = models.UUIDField(primary_key=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)

    @property
    def age(self):
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )


class BalanceSheet(models.Model):
    """
    A balance sheet for a person.
    """

    id = models.UUIDField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    date_calculated = models.DateTimeField(null=False)
    assets = models.BigIntegerField(null=False, default=0)
    liabilities = models.BigIntegerField(null=False, default=0)

    def calculate_net_worth(self) -> int:
        return self.assets - self.liabilities

    class Meta:
        ordering = ["person_id", "-date_calculated"]
