from dataclasses import dataclass
from decimal import Decimal
from typing import Union

from stonky.typedef import CurrencyStr, SortStr, assert_never


@dataclass
class Stock:
    ticket: str = ""
    currency: CurrencyStr = "USD"
    current_amount: float = 0.0
    delta_amount: float = 0.0
    delta_percent: float = 0.0
    market_price: float = 0.0
    volume: float = 0.0

    def __post_init__(self) -> None:
        self.ticket = self.ticket.upper()

    @property
    def volume_str(self) -> str:
        if self.volume >= 1_000_000_000:
            d = Decimal(self.volume / 1_000_000_000).quantize(
                Decimal(".1"), rounding="ROUND_DOWN"
            )
            s = str(d).rstrip(".0") + "B"
        elif self.volume >= 1_000_000:
            d = Decimal(self.volume / 1_000_000).quantize(
                Decimal(".1"), rounding="ROUND_DOWN"
            )
            s = str(d).rstrip(".0") + "M"
        elif self.volume >= 1_000:
            d = Decimal(self.volume / 1_000).quantize(
                Decimal(".1"), rounding="ROUND_DOWN"
            )
            s = str(d).rstrip(".0") + "K"
        elif self.volume == 0:
            s = ""
        else:
            s = f"{self.volume:.2f}"
        return s

    @property
    def colour(self) -> str:
        if self.delta_amount < 0:
            return "red"
        elif self.delta_amount == 0:
            return "yellow"
        else:
            return "green"

    def increase_count(self, count: float):
        self.delta_amount *= count
        self.current_amount *= count

    def convert_currency(self, conversion_rate: float):
        self.current_amount *= conversion_rate
        self.delta_amount *= conversion_rate

    def sort_value(self, sort_key: SortStr) -> Union[float, str]:
        if sort_key == "amount" or sort_key == "amount_desc":
            return self.current_amount
        elif sort_key == "ticket" or sort_key == "ticket_desc":
            return self.ticket
        elif sort_key == "change" or sort_key == "change_desc":
            return self.delta_percent
        elif sort_key == "volume" or sort_key == "volume_desc":
            return self.volume
        else:
            assert_never(sort_key)
