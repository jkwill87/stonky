from argparse import ArgumentParser
from configparser import ConfigParser
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional
from stonky.types import SortType


@dataclass
class Config:
    positions: Dict[str, int] = field(default_factory=dict)
    watchlist: List[str] = field(default_factory=list)
    config_path: Path = Path.home() / ".stonky.cfg"
    refresh: Optional[int] = None
    sort: Optional[SortType] = SortType.CHANGE
    currency: Optional[str] = None

    @property
    def all_tickets(self):
        return set(self.positions.keys()) | set(self.watchlist)

    def __post_init__(self):
        self._get_args()
        self._get_config()

    def _get_args(self):
        parser = ArgumentParser()
        parser.add_argument("--config")
        parser.add_argument("--currency", type=int)
        parser.add_argument("--refresh", type=int)
        parser.add_argument("--sort", choices=SortType.arg_choices())
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
        parser = ConfigParser(allow_no_value=True)
        parser.read_string(self.config_path.read_text())
        if "positions" in parser._sections:
            for ticket, amount in parser._sections["positions"].items():
                self.positions[ticket] = int(amount)
        if "watchlist" in parser._sections:
            self.watchlist += parser._sections["watchlist"]
        if parser.get("preferences", "refresh", fallback=None):
            self.refresh = int(parser.get("preferences", "refresh"))
        if parser.get("preferences", "currency", fallback=None):
            self.currency = parser.get("preferences", "currency").upper()
