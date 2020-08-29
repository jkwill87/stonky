from enum import Enum

from typing import Optional, Tuple


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
    def arg_choices(cls) -> Tuple[str]:
        return *tuple(str(choice.value) for choice in cls), ""


class SortType(Enum):
    AMOUNT = "amount_current"
    AMOUNT_DESC = "amount_current_desc"
    TICKET = "ticket"
    TICKET_DESC = "ticket_desc"
    LOW = "amount_low"
    LOW_DESC = "amount_low_desc"
    HIGH = "amount_high"
    HIGH_DESC = "amount_high_desc"
    CLOSE = "amount_prev_close"
    CLOSE_DESC = "amount_prev_close_desc"
    CHANGE = "delta_percent"
    CHANGE_DESC = "delta_percent_desc"
    VOLUME = "volume"
    VOLUME_DESC = "volume_desc"

    @classmethod
    def from_arg(cls, arg: str) -> Optional["SortType"]:
        return cls.__members__.get(arg.upper(), None)

    @classmethod
    def arg_choices(cls) -> Tuple[str]:
        return *tuple(member.lower() for member in cls.__members__), ""
