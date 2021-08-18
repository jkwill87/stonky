from enum import Enum
from typing import Generator, Optional

# TODO: Create a currency dataclass which holds name, symbol, format fn, arithmetics
# TODO: Add a lookup method to find by string; incorporate _missing_ logic
class CurrencyType(Enum):
    AUD = "AUD"
    BGN = "BGN"
    BRL = "BRL"
    CAD = "CAD"
    CHF = "CHF"
    CNY = "CNY"
    CZK = "CZK"
    DKK = "DKK"
    EUR = "EUR"
    GBP = "GBP"
    HKD = "HKD"
    HRK = "HRK"
    HUF = "HUF"
    IDR = "IDR"
    ILS = "ILS"
    INR = "INR"
    ISK = "ISK"
    JPY = "JPY"
    KRW = "KRW"
    MXN = "MXN"
    MYR = "MYR"
    NOK = "NOK"
    NZD = "NZD"
    PHP = "PHP"
    PLN = "PLN"
    RON = "RON"
    RUB = "RUB"
    SEK = "SEK"
    SGD = "SGD"
    THB = "THB"
    TRY = "TRY"
    USD = "USD"
    ZAR = "ZAR"

    @classmethod
    def _missing_(cls, name):
        for member in cls:
            if member.name == name.upper():
                return member

    @classmethod
    def arg_choices(cls) -> Generator[str, None, None]:
        yield from (str(choice.value) for choice in cls)
        yield ""


class SortType(Enum):
    AMOUNT = "current_amount"
    AMOUNT_DESC = "current_amount_desc"
    TICKET = "ticket"
    TICKET_DESC = "ticket_desc"
    CHANGE = "delta_percent"
    CHANGE_DESC = "delta_percent_desc"
    VOLUME = "volume"
    VOLUME_DESC = "volume_desc"

    @classmethod
    def from_arg(cls, arg: str) -> Optional["SortType"]:
        return cls.__members__.get(arg.upper(), None)

    @classmethod
    def arg_choices(cls) -> Generator[str, None, None]:
        yield from (member.lower() for member in cls.__members__)
        yield ""
