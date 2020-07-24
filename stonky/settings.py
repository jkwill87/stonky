from argparse import ArgumentParser
from configparser import ConfigParser
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, get_type_hints

from stonky.forex import Forex
from stonky.types import SortType


@dataclass
class Settings:
    positions: Dict[str, int] = field(default_factory=dict)
    watchlist: List[str] = field(default_factory=list)
    config_path: Path = Path.home() / ".stonky.cfg"
    cash: Dict[str, float] = field(default_factory=dict)
    refresh: Optional[float] = None
    sort: Optional[SortType] = SortType.CHANGE
    currency: Optional[str] = None

    @property
    def all_tickets(self):
        return set(self.positions.keys()) | set(self.watchlist)

    def __post_init__(self):
        self._get_args()
        self._get_config()

    def _get_args(self):
        parser = ArgumentParser(prog="stonky")
        parser.add_argument(
            "--config", metavar="PATH", help="sets path to config file"
        )
        parser.add_argument(
            "--currency",
            metavar="CODE",
            choices=get_type_hints(Forex).keys(),
            help="converts all amounts using current forex rates",
        )
        parser.add_argument(
            "--refresh",
            metavar="SECONDS",
            type=int,
            help="refreshes output on set interval",
        )
        parser.add_argument(
            "--sort",
            metavar="FIELD",
            choices=SortType.arg_choices(),
            help="orders stocks by field",
        )
        args = parser.parse_args()
        if args.config:
            self.config_path = Path(args.config)
        if args.currency:
            self.currency = args.currency
        if args.refresh:
            self.refresh = args.refresh
        if args.sort:
            self.sort = SortType.from_arg(args.sort)

    def _get_config(self):
        parser = ConfigParser(
            allow_no_value=True, inline_comment_prefixes=(";", "#")
        )
        parser.read_string(self.config_path.read_text())
        if "positions" in parser:
            for ticket, amount in parser.items("positions"):
                self.positions[ticket.upper()] = float(amount)
        if "watchlist" in parser:
            self.watchlist += [
                line[0].upper() for line in parser.items("watchlist")
            ]
        if "cash" in parser:
            for currency_code, amount in parser.items("cash"):
                self.cash[currency_code.upper()] = float(amount)
        if parser.get("preferences", "refresh", fallback=None):
            self.refresh = float(parser.get("preferences", "refresh"))
        if parser.get("preferences", "currency", fallback=None):
            self.currency = parser.get("preferences", "currency").upper()
