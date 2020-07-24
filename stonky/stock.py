from dataclasses import dataclass
from decimal import Decimal

from stonky.forex import Forex


@dataclass
class Stock:
    ticket: str = ""
    currency_code: str = "USD"
    amount_bid: float = 0
    amount_ask: float = 0
    amount_low: float = 0
    amount_high: float = 0
    amount_prev_close: float = 0
    delta_amount: float = 0
    delta_percent: float = 0
    volume: float = 0

    def __post_init__(self):
        self.ticket = self.ticket.upper()
        self.currency_code = self.currency_code.upper()

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
        s += self.volume_str.ljust(8)
        s += "@ " + f"{self.amount_bid:.2f}".ljust(8)
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
        return f"{self.delta_percent*100:+.2f}% {self.delta_amount:+,.2f} {self.currency_code}"

    def convert_currency(self, forex: Forex, currency_code: str):
        if self.currency_code == currency_code:
            return self
        rate = 1.0 / getattr(forex, self.currency_code)
        self.currency_code = currency_code
        self.amount_bid *= rate
        self.amount_ask *= rate
        self.amount_low *= rate
        self.amount_high *= rate
        self.amount_prev_close *= rate
