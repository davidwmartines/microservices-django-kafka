import logging

from cloudevents.abstract import AnyCloudEvent
from points.models import Order, Customer

from events.handlers import CloudEventHandler

logger = logging.getLogger(__name__)


class CustomerEventHandler(CloudEventHandler):
    """
    Handles Customer events from Kafka
    by upserting a record into this service's local database.

    The incoming events are deserialized using the canonical Customer
    schema defined in the specified avsc file.
    """

    def __init__(self) -> None:
        super().__init__(event_name="customer_entity_state")

    def handle(self, event: AnyCloudEvent) -> None:
        data = event.data

        obj, created = Customer.objects.update_or_create(
            id=data["id"],
            defaults={
                "date_established": data["date_established"]
                if "date_established" in data
                else None,
            },
        )
        logger.info(f"persisted record for customer {obj.id}. created: {created}")


class OrderEventHandler(CloudEventHandler):
    """
    Handles Order events from Kafka
    by creating an order record in this service's local database.
    """

    def __init__(self) -> None:
        super().__init__(event_name="order_created")

    def handle(self, event: AnyCloudEvent) -> None:
        data = event.data

        customer_id = data["customer_id"]

        if not Customer.objects.filter(pk=customer_id).exists():
            raise Exception(f"unknown customer {customer_id}")

        # logically, this would be saving a new orders since they are
        # immutable instances.  However, using update_or_create to safely handle
        # duplicate events.
        obj, created = Order.objects.update_or_create(
            id=data["id"],
            defaults={
                "customer_id": customer_id,
                "date_placed": data["date_placed"],
                "item_count": data["item_count"],
            },
        )
        logger.info(
            f"persisted order {obj.id} for customer {customer_id}. created: {created}"
        )
