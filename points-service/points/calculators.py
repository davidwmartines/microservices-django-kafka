from typing import NamedTuple
from points.models import Customer


class Award(NamedTuple):
    points: float


class PointsCalculator:
    __slots__ = "customer"

    def __init__(self, customer: Customer) -> None:
        assert customer
        self.customer = customer

    def award(self) -> Award:
        total_items = 0
        for order in self.customer.order_set.all():
            total_items += order.item_count

        return Award(points=total_items / 42)
