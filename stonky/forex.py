from dataclasses import dataclass
from typing import get_type_hints


@dataclass
class Forex:
    AUD: float = 1.0
    BRL: float = 1.0
    CAD: float = 1.0
    CHF: float = 1.0
    CNY: float = 1.0
    CZK: float = 1.0
    DKK: float = 1.0
    EUR: float = 1.0
    GBP: float = 1.0
    HKD: float = 1.0
    HRK: float = 1.0
    HUF: float = 1.0
    IDR: float = 1.0
    ILS: float = 1.0
    INR: float = 1.0
    ISK: float = 1.0
    JPY: float = 1.0
    KRW: float = 1.0
    MXN: float = 1.0
    MYR: float = 1.0
    NOK: float = 1.0
    NZD: float = 1.0
    PHP: float = 1.0
    PLN: float = 1.0
    RON: float = 1.0
    RUB: float = 1.0
    SEK: float = 1.0
    SGD: float = 1.0
    THB: float = 1.0
    TRY: float = 1.0
    USD: float = 1.0
    ZAR: float = 1.0

    @classmethod
    def keys(cls):
        return list(get_type_hints(cls).keys())
