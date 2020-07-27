from enum import Enum

from typing import Optional, Tuple


class SortType(Enum):
    AMOUNT = "amount_current"
    AMOUNT_DESC = "amount_desc"
    TICKET = "ticket"
    TICKET_DESC = "ticket_desc"
    LOW = "amount_low"
    LOW_DESC = "amount_low_desc"
    HIGH = "amount_high"
    HIGH_DESC = "high_desc"
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
        return tuple(member.lower() for member in cls.__members__)
