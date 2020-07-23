from argparse import ArgumentParser
from configparser import ConfigParser
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Config:
    positions: Dict[str, int] = field(default_factory=dict)
    watchlist: List[str] = field(default_factory=list)
    ticket: Optional[str] = None
    polling: Optional[int] = None
    config_path: Path = Path.home() / ".stonky.cfg"
    sort_key = "delta_percent"
    conversion_currency = None

    @property
    def all_tickets(self):
        return set(self.positions.keys()) | set(self.watchlist)

    def __post_init__(self):
        self._get_args()
        if self.config_path.exists():
            self._get_config()
        if self.conversion_currency:
            self.conversion_currency = self.conversion_currency.upper()

    def _get_args(self):
        parser = ArgumentParser()
        parser.add_argument("--config")
        args = parser.parse_args()
        if args.config:
            self.config_path = Path(args.config)

    def _get_config(self):
        parser = ConfigParser(allow_no_value=True)
        parser.read_string(self.config_path.read_text())
        if "positions" in parser._sections:
            for ticket, amount in parser._sections["positions"].items():
                self.positions[ticket] = int(amount)
        if "watchlist" in parser._sections:
            self.watchlist += parser._sections["watchlist"]
        if parser.get("preferences", "polling", fallback=None):
            self.polling = int(parser.get("preferences", "polling"))
        if parser.get("preferences", "conversion_currency", fallback=None):
            self.conversion_currency = parser.get("preferences", "conversion_currency").upper()
