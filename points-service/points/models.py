from django.db import models


class Customer(models.Model):
    """
    Represents a customer known to the Points Service.
    Customer data comes from the microservice ecosystem
    via the customer entity state stream.  The customer data
    in this service is not considered authoritative and
    is not managed here.
    """

    id = models.UUIDField(primary_key=True)
    date_established = models.DateTimeField(null=True, blank=True)


class Order(models.Model):
    """
    An order for a customer.
    """

    id = models.UUIDField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_placed = models.DateTimeField(null=False)
    item_count = models.BigIntegerField(null=False, default=0)

    class Meta:
        ordering = ["customer_id", "-date_placed"]
