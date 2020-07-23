from typing import List

from teletype.io import style_format, erase_lines, style_print

from stonky.config import Config
from stonky.stock_store import StockStore
from time import sleep


class View:
    def __init__(self, config: Config, stock_store: StockStore):
        self.config = config
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
        if self.config.watchlist:
            lines += self.watchlist

        if self.config.positions:
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
                    remaining = self.config.polling
                    self.stock_store.update_stocks()
                    erase_lines(self._draw_buffer + 3)
                    self.draw()
                else:
                    erase_lines(3)
                    remaining -= 1
                style_print(f"\nrefreshing in {remaining}", style="blue")
                style_print("press CTRL-C to quit", style="blue")
                sleep(1)
        except KeyboardInterrupt:
            pass
