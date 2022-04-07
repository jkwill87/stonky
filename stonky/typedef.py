from typing import Any, Tuple

from typing_extensions import Literal, NoReturn, TypeGuard, get_args

CurrencyStr = Literal[
    "AUD",
    "BGN",
    "BRL",
    "CAD",
    "CHF",
    "CNY",
    "CZK",
    "DKK",
    "EUR",
    "GBP",
    "HKD",
    "HRK",
    "HUF",
    "IDR",
    "ILS",
    "INR",
    "ISK",
    "JPY",
    "KRW",
    "MXN",
    "MYR",
    "NOK",
    "NZD",
    "PHP",
    "PLN",
    "RON",
    "RUB",
    "SEK",
    "SGD",
    "THB",
    "TRY",
    "USD",
    "ZAR",
]
CURRENCY_CHOICES: Tuple[CurrencyStr, ...] = get_args(CurrencyStr)


def is_currency_str(value: Any) -> TypeGuard[CurrencyStr]:
    return value in CURRENCY_CHOICES


SortStr = Literal[
    "amount",
    "amount_desc",
    "ticket",
    "ticket_desc",
    "change",
    "change_desc",
    "volume",
    "volume_desc",
]
SORT_CHOICES: Tuple[SortStr, ...] = get_args(SortStr)


def is_sort_str(value: Any) -> TypeGuard[SortStr]:
    return value in SORT_CHOICES


def assert_never(value: NoReturn) -> NoReturn:
    assert False, f"Unhandled value: {value} ({type(value).__name__})"
