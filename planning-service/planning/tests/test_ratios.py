from datetime import datetime, timezone
from uuid import uuid4

from django.test import TestCase
from planning.models import Person
from planning.ratios import NetWorthToTotalAssets


class NetWorthToTotalAssets_Age42(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.as_of = datetime(2022, 12, 31, tzinfo=timezone.utc)
        cls.person = Person.objects.create(
            id=uuid4(), date_of_birth=datetime(1980, 2, 23, tzinfo=timezone.utc)
        )
        cls.person.balancesheet_set.create(
            id=uuid4(),
            assets=250,
            liabilities=100,
            date_calculated=cls.as_of,
        )
        cls.result = NetWorthToTotalAssets(cls.person, as_of=cls.as_of).result

    def test_ratio(self):
        self.assertEqual(0.6, self.result.ratio)

    def test_benchmark(self):
        self.assertEqual(0.5, self.result.benchmark)

    def test_status(self):
        self.assertEqual("Good", self.result.status)


class NetWorthToTotalAssets_Age66(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.as_of = datetime(2022, 12, 31, tzinfo=timezone.utc)
        cls.person = Person.objects.create(
            id=uuid4(), date_of_birth=datetime(1956, 5, 12, tzinfo=timezone.utc)
        )
        cls.person.balancesheet_set.create(
            id=uuid4(),
            assets=250,
            liabilities=100,
            date_calculated=cls.as_of,
        )
        cls.result = NetWorthToTotalAssets(cls.person, as_of=cls.as_of).result

    def test_ratio(self):
        self.assertEqual(0.6, self.result.ratio)

    def test_benchmark(self):
        self.assertEqual(0.75, self.result.benchmark)

    def test_status(self):
        self.assertEqual("Needs improvement", self.result.status)
