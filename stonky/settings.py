from argparse import ArgumentParser, RawTextHelpFormatter
from configparser import ConfigParser
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from pkg_resources import resource_filename

from stonky.const import EPILOG
from stonky.enums import CurrencyType, SortType
from stonky.exceptions import StonkyException


@dataclass
class Settings:
    positions: Dict[str, float] = field(default_factory=dict)
    watchlist: List[str] = field(default_factory=list)
    config_path: Path = Path.home() / ".stonky.cfg"
    cash: Dict[CurrencyType, float] = field(default_factory=dict)
    refresh: Optional[float] = None
    sort: Optional[SortType] = SortType.CHANGE
    currency: Optional[CurrencyType] = None

    @classmethod
    def load(cls, **kwargs):
        settings = cls(**kwargs)
        settings._get_args()
        settings._get_config()
        settings._apply_parsed_args()
        return settings

    def _get_args(self):
        parser = ArgumentParser(
            prog="stonky", epilog=EPILOG, formatter_class=RawTextHelpFormatter
        )
        parser.add_argument(
            "--config", metavar="PATH", help="sets path to config file"
        )
        parser.add_argument(
            "--currency",
            metavar="CODE",
            choices=CurrencyType.arg_choices(),
            type=str.upper,
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
            type=str.lower,
            choices=SortType.arg_choices(),
            help="orders stocks by field",
        )
        self._args = parser.parse_args()
        if self._args.config:
            self.config_path = Path(self._args.config)

    def _apply_parsed_args(self):
        if self._args.currency == "":
            self.currency = None
        elif self._args.currency:
            self.currency = CurrencyType(self._args.currency)
        if self._args.refresh in ("", 0):
            self.refresh = None
        elif self._args.refresh:
            self.refresh = self._args.refresh
        if self._args.sort == "":
            self._args.sort = None
        elif self._args.sort is not None:
            self.sort = SortType.from_arg(self._args.sort)

    def _get_config(self):
        parser = ConfigParser(
            allow_no_value=True, inline_comment_prefixes=(";", "#")
        )
        if not self.config_path.exists():
            self.config_path = Path(
                resource_filename("stonky", "__example.cfg")
            )
        parser.read_string(self.config_path.read_text())
        if "positions" in parser:
            for ticket, amount in parser.items("positions"):
                amount = float(amount.replace(",", ""))
                self.positions[ticket.upper()] = amount
        if "watchlist" in parser:
            tickets = [line[0].upper() for line in parser.items("watchlist")]
            self.watchlist += tickets
        if "cash" in parser:
            for currency, amount in parser.items("cash"):
                try:
                    currency = CurrencyType(currency.upper())
                except ValueError:
                    raise StonkyException(
                        f"{currency} is an invalid currency code"
                    )
                amount = float(amount.replace(",", ""))
                self.cash[currency] = amount
        if parser.get("preferences", "refresh", fallback=None):
            self.refresh = float(parser.get("preferences", "refresh"))
        if parser.get("preferences", "currency", fallback=None):
            currency = parser.get("preferences", "currency").upper()
            try:
                self.currency = CurrencyType(currency)
            except ValueError:
                raise StonkyException(f"{currency} is an invalid currency code")
