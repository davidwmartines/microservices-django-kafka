from planning.models import Person
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import NamedTuple


class CalculatedRatio(NamedTuple):
    """
    The results of a financial ratio calculation.
    """

    ratio: float
    """
    The calculated ratio value.
    """

    benchmark: float
    """
    The benchmark value for the person based on their demographics.
    """

    status: str
    """
    Textual description evaluating the ratio for the person.
    """


class FinancialRatioCalculator(ABC):
    """
    Base class for Finanacial Ratio Calculators
    """

    @property
    @abstractmethod
    def result(self) -> CalculatedRatio:
        raise NotImplementedError()

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()


class NetWorthToTotalAssets(FinancialRatioCalculator):
    _benchmarks = {(0, 30): 0.20, (31, 45): 0.50, (46, 66): 0.75, (67, 999): 0.90}
    """
    Benchmark ratios for age ranges (mostly made up...)
    """

    __slots__ = "person", "as_of"

    def __init__(
        self, person: Person, as_of: datetime = datetime.now(timezone.utc)
    ) -> None:
        assert person
        self.person = person
        self.as_of = as_of

    @property
    def name(self) -> str:
        return "Net Worth to Total Assets"

    @property
    def result(self) -> CalculatedRatio:
        # get latest balance sheet
        balance_sheet = (
            self.person.balancesheet_set.order_by("-date_calculated")
            .filter(date_calculated__lte=self.as_of)
            .first()
        )

        if balance_sheet is None:
            print(f"NO BALANCE SHEET as of {self.as_of}")
            return None

        # get net worth
        net_worth = balance_sheet.calculate_net_worth()

        # get ratio
        ratio = net_worth / balance_sheet.assets

        # determine good benchmark for the person
        benchmark = next(
            iter(
                {
                    k: v
                    for (k, v) in self._benchmarks.items()
                    if k[0] <= self.person.age(self.as_of) <= k[1]
                }.items()
            ),
            None,
        )
        benchmark_ratio = benchmark[1] if benchmark is not None else None

        # evaluate
        if benchmark_ratio is not None:
            if ratio < benchmark_ratio:
                evaluation = "Needs improvement"
            else:
                evaluation = "Good"

        return CalculatedRatio(
            ratio=ratio, benchmark=benchmark_ratio, status=evaluation
        )
