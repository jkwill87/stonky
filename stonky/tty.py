from time import sleep
from traceback import format_exc
from typing import List

from teletype.io import erase_lines, style_format, style_print

from stonky.const import SYSTEM
from stonky.settings import Settings
from stonky.stock_store import StockStore


class Tty:
    def __init__(self, settings: Settings, stock_store: StockStore):
        self.settings = settings
        self.stock_store = stock_store
        self._draw_buffer = 0

    @property
    def watchlist(self) -> List[str]:
        lines = [style_format("WATCHLIST", style="bold")]
        for stock in self.stock_store.watchlist:
            lines.append(style_format(stock.ticker_tape, stock.colour))
        return lines

    @property
    def positions(self) -> List[str]:
        lines = [style_format("POSITIONS", style="bold")]
        for stock in self.stock_store.positions:
            lines.append(style_format(stock.position, stock.colour))
        return lines

    @property
    def profit_and_loss(self) -> List[str]:
        lines = [style_format("PROFIT AND LOSS", style="bold")]
        for stock in self.stock_store.profit_and_loss:
            lines.append(style_format(stock.profit_and_loss, stock.colour))
        return lines

    @property
    def balances_str(self) -> List[str]:
        lines = [style_format("BALANCES", style="bold")]
        for currency, balance in self.stock_store.balances.items():
            lines.append(f"{balance:,.2f} {currency}")
        return lines

    def draw(self):
        lines = []
        if self.settings.watchlist:
            lines += self.watchlist

        if self.settings.positions:
            lines.append("")
            lines += self.positions
            lines.append("")
            lines += self.profit_and_loss
            lines.append("")
            lines += self.balances_str
        self._draw_buffer = len(lines)
        print("\n".join(lines))

    def draw_live(self):
        remaining = 0
        try:
            while True:
                if remaining == 0:
                    remaining = self.settings.refresh
                    self.stock_store.update_stocks()
                    erase_lines(self._draw_buffer)
                    self.draw()
                    self._draw_buffer += 3
                else:
                    erase_lines(3)
                    remaining -= 1
                style_print(f"\nrefreshing in {remaining}", style="cyan")
                style_print("press CTRL-C to quit", style="cyan")
                sleep(1)
        except KeyboardInterrupt:
            pass


def crash_report():
    system_information_str = "\n".join(
        [f" - {k} = {getattr(v, 'value', v)}" for k, v in SYSTEM.items()]
    )
    s = f"""
============================== CRASH REPORT BEGIN ==============================

--------------------------------- environment ----------------------------------

{system_information_str}

--------------------------------- stack trace ----------------------------------

{format_exc()}
=============================== CRASH REPORT END ===============================

Dang, it looks like stonky crashed! Please consider filling an issue at
https://github.com/jkwill87/stonky/issues along with this report.
"""
    print(s)
    raise SystemExit(1)
