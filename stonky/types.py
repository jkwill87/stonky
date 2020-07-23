from enum import Enum

from typing import Optional, Tuple


class SortType(Enum):
    TICKET = "ticket"
    BID = "amount_bid"
    ASK = "amount_ask"
    LOW = "amount_low"
    HIGH = "amount_high"
    CLOSE = "amount_prev_close"
    CHANGE = "delta_percent"
    VOLUME = "volume"

    @classmethod
    def from_arg(cls, arg: str) -> Optional["SortType"]:
        return cls.__members__.get(arg.upper(), None)

    @classmethod
    def arg_choices(cls) -> Tuple[str]:
        return tuple(member.lower() for member in cls.__members__)
