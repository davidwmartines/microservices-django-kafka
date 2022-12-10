from django.db import models
from uuid import uuid4
from datetime import datetime


class Order(models.Model):
    """
    Represents a simple order for a customer,
    placed on a specific date.
    """

    id = models.UUIDField(primary_key=True, default=uuid4)
    customer_id = models.UUIDField(null=False)
    date_placed = models.DateTimeField(null=False, default=datetime.utcnow)
    item_count = models.BigIntegerField(null=False, default=0)
