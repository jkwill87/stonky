from dataclasses import dataclass
from decimal import Decimal

from stonky.enums import CurrencyType


@dataclass
class Stock:
    ticket: str = ""
    currency: CurrencyType = CurrencyType.USD
    amount_bid: float = 0.0
    amount_ask: float = 0.0
    amount_low: float = 0.0
    amount_high: float = 0.0
    amount_prev_close: float = 0.0
    delta_amount: float = 0.0
    delta_percent: float = 0.0
    market_price: float = 0.0
    volume: float = 0.0

    def __post_init__(self):
        self.ticket = self.ticket.upper()

    def __str__(self):
        return self.ticker_tape

    @property
    def amount_current(self):
        if self.amount_bid:
            return self.amount_bid
        elif self.market_price:
            return self.market_price
        else:
            return 0.0

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
    def colour(self):
        if self.delta_amount < 0:
            return "red"
        elif self.delta_amount == 0:
            return "yellow"
        else:
            return "green"

    @property
    def ticker_tape(self) -> str:
        if self.delta_amount < 0:
            symbol = "▼"
        elif self.delta_amount == 0:
            symbol = "▬"
        else:
            symbol = "▲"
        s = self.ticket.ljust(8)
        if self.volume:
            s += self.volume_str.ljust(8) + "@ "
        else:
            s += " " * 8
        s += f"{self.amount_current:.2f}".ljust(8)
        s += symbol
        s += f"{self.delta_amount:+,.2f} {self.delta_percent*100:+.2f}%".rjust(
            15
        )
        return s

    @property
    def position(self) -> str:
        s = self.ticket.ljust(8)
        s += f"{self.delta_amount:+,.2f}".ljust(8)
        s += f"{self.delta_percent*100:+.2f}%"
        return s

    @property
    def profit_and_loss(self) -> str:
        return f"{self.delta_percent*100:+.2f}% {self.delta_amount:+,.2f} {self.currency.value}"

    def increase_count(self, count: float):
        self.delta_amount *= count
        self.amount_prev_close *= count

    def convert_currency(self, conversion_rate: float):
        self.amount_bid *= conversion_rate
        self.amount_ask *= conversion_rate
        self.amount_low *= conversion_rate
        self.amount_high *= conversion_rate
        self.amount_prev_close *= conversion_rate
        self.delta_amount *= conversion_rate
        self.market_price *= conversion_rate
