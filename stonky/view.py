from teletype.io import style_format

from stonky.config import Config
from stonky.stock_store import StockStore


class View:
    def __init__(self, config: Config, stock_store: StockStore):
        self.config = config
        self.stock_store = stock_store

    @property
    def watchlist(self) -> str:
        lines = [style_format("WATCHLIST", style="bold")]
        for stock in self.stock_store.watchlist:
            lines.append(style_format(stock.ticker_tape, stock.colour))
        return "\n".join(lines)

    @property
    def positions(self):
        lines = [style_format("POSITIONS", style="bold")]
        for stock in self.stock_store.positions:
            lines.append(style_format(stock.position, stock.colour))
        return "\n".join(lines)

    @property
    def profit_and_loss(self):
        lines = [style_format("PROFIT AND LOSS", style="bold")]
        for stock in self.stock_store.profit_and_loss:
            lines.append(style_format(stock.profit_and_loss, stock.colour))
        return "\n".join(lines)

    @property
    def balances_str(self):
        lines = [style_format("BALANCES", style="bold")]
        for currency, balance in self.stock_store.balances.items():
            lines.append(f"{balance:,.2f} {currency}")
        return "\n".join(lines)
