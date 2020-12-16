import asyncio
from traceback import format_exc
from typing import List

from teletype.io import erase_lines, style_format, style_print

from stonky.const import SYSTEM
from stonky.settings import Settings
from stonky.stock_store import StockStore


def format_table(rows: List[List[str]], colours: List[str]):
    column_widths = [
        len(max(columns, key=len))
        for columns in [list(column) for column in zip(*rows)]
    ]
    return [
        style_format(
            " ".join(
                [
                    col.ljust(column_widths[idx_col] + 1)
                    for idx_col, col in enumerate(row)
                ]
            ),
            colours[idx],
        )
        for idx, row in enumerate(rows)
    ]


class Tty:
    def __init__(self, settings: Settings, stock_store: StockStore):
        self.settings = settings
        self.stock_store = stock_store
        self._draw_buffer = 0

    @property
    def watchlist(self) -> List[str]:
        rows = []
        colours = []
        for stock in self.stock_store.watchlist:
            row = []
            row.append(stock.ticket)
            if stock.volume:
                row.append(stock.volume_str)
            else:
                row.append("")
            row.append(f"@ {stock.amount_current:.2f}")
            if stock.delta_amount < 0:
                symbol = "▼"
            elif stock.delta_amount == 0:
                symbol = "▬"
            else:
                symbol = "▲"
            row.append(symbol)
            row.append(f"{stock.delta_amount:+,.2f}")
            row.append(f"{stock.delta_percent*100:+.2f}%")
            rows.append(row)
            colours.append(stock.colour)
        return [style_format("WATCHLIST", style="bold")] + format_table(
            rows, colours
        )

    @property
    def positions(self) -> List[str]:
        rows = []
        colours = []
        for stock in self.stock_store.positions:
            row = [
                stock.ticket,
                f"{stock.delta_amount:+,.2f}",
                f"{stock.delta_percent*100:+.2f}%",
            ]
            rows.append(row)
            colours.append(stock.colour)
        return [style_format("POSITIONS", style="bold")] + format_table(
            rows, colours
        )

    @property
    def profit_and_loss(self) -> List[str]:
        lines = [style_format("PROFIT AND LOSS", style="bold")]
        for stock in self.stock_store.profit_and_loss:
            lines.append(
                style_format(
                    f"{stock.delta_percent*100:+.2f}% {stock.delta_amount:+,.2f} {stock.currency.value}",
                    stock.colour,
                )
            )
        return lines

    @property
    def balances_str(self) -> List[str]:
        lines = [style_format("BALANCES", style="bold")]
        for currency, balance in self.stock_store.balances.items():
            lines.append(f"{balance:,.2f} {currency.value}")
        return lines

    async def draw(self):
        lines = []
        await self.stock_store.update()
        if self.settings.watchlist:
            lines += self.watchlist

        if self.settings.positions:
            lines.append("")
            lines += self.positions
            lines.append("")
            lines += self.profit_and_loss
            lines.append("")
            lines += self.balances_str
        if self._draw_buffer:
            erase_lines(self._draw_buffer)
        self._draw_buffer = len(lines)
        print("\n".join(lines))

    async def draw_live(self):
        remaining = 0
        while True:
            if remaining == 0:
                remaining = self.settings.refresh
                await self.draw()
                self._draw_buffer += 3
            else:
                erase_lines(3)
                remaining -= 1
            style_print(f"\nrefreshing in {remaining}", style="cyan")
            style_print("press CTRL-C to quit", style="cyan")
            await asyncio.sleep(1)


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
