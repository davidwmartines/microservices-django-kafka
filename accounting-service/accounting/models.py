from django.db import models
from uuid import uuid4
from datetime import datetime


class BalanceSheet(models.Model):
    """
    Represents a simple balance sheet for a person,
    calculated on a specific date.

    A balance sheet is considered immutable once created.

    The accounting service is the system of record
    for producing balance sheets.
    """

    id = models.UUIDField(primary_key=True, default=uuid4)
    person_id = models.UUIDField(null=False, unique_for_date="date_calculated")
    date_calculated = models.DateTimeField(null=False, default=datetime.utcnow)
    assets = models.BigIntegerField(null=False, default=0)
    liabilities = models.BigIntegerField(null=False, default=0)
