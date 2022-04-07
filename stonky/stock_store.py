import asyncio
from copy import copy
from typing import Dict, List, Optional, Set

from stonky.api import Api
from stonky.settings import Settings
from stonky.stock import Stock
from stonky.typedef import CurrencyStr, SortStr, is_sort_str


class StockStore:
    def __init__(self, api: Api, settings: Settings):
        self._stocks: Dict[str, Stock] = {}
        self._api: Api = api
        self._sort: Optional[SortStr] = settings.sort
        self._base_currency: Optional[CurrencyStr] = settings.currency
        self._settings: Settings = settings
        self._raw_cash: Dict[CurrencyStr, float] = {}
        self._raw_positions: Dict[str, float] = {}
        self._raw_watchlist: List[str] = []
        self._raw_tickets: Set[str] = set()

    async def update(self):
        self._reset_raw_values()
        await self._update_quotes()
        if self._base_currency:
            await self._convert_currencies()

    @property
    def watchlist(self) -> List[Stock]:
        return self._try_sort(
            [
                stock
                for ticket, stock in self._stocks.items()
                if ticket in self._raw_watchlist
            ]
        )

    @property
    def positions(self) -> List[Stock]:
        results = []
        for ticket, count in self._raw_positions.items():
            stock = copy(self._stocks[ticket])
            stock.increase_count(count)
            results.append(stock)
        return self._try_sort(results)

    @property
    def profit_and_loss(self) -> List[Stock]:
        pnl = {}
        for ticket, count in self._raw_positions.items():
            stock = copy(self._stocks[ticket])
            stock.increase_count(count)
            if stock.currency not in pnl:
                pnl[stock.currency] = stock
            else:
                pnl[stock.currency].current_amount += stock.current_amount
                pnl[stock.currency].delta_amount += stock.delta_amount
        results = []
        for pnl_line in pnl.values():
            pnl_line.delta_percent = pnl_line.delta_amount / pnl_line.current_amount
            results.append(pnl_line)
        return results

    @property
    def balances(self) -> Dict[CurrencyStr, float]:
        balances = {}
        for ticket, count in self._raw_positions.items():
            stock = self._stocks[ticket]
            if stock.currency not in balances:
                balances[stock.currency] = stock.current_amount * count
            else:
                balances[stock.currency] += stock.current_amount * count
        for currency, amount in self._raw_cash.items():
            if currency not in balances:
                balances[currency] = amount
            else:
                balances[currency] += amount
        return balances

    def _try_sort(self, stocks: List[Stock]):
        if is_sort_str(self._sort):
            sort_by = self._sort
            reverse = sort_by.endswith("_desc")
            stocks.sort(key=lambda stock: stock.sort_value(sort_by), reverse=reverse)
        return stocks

    def _reset_raw_values(self) -> None:
        self._raw_cash = copy(self._settings.cash)
        self._raw_positions = copy(self._settings.positions)
        self._raw_watchlist = copy(self._settings.watchlist)
        self._raw_tickets = set(self._settings.positions) | set(
            self._settings.watchlist
        )

    async def _update_quotes(self):
        if not self._raw_tickets:
            return
        futures = tuple(self._api.get_quote(ticket) for ticket in self._raw_tickets)
        self._stocks = {stock.ticket: stock for stock in await asyncio.gather(*futures)}

    async def _convert_currencies(self):
        assert self._base_currency is not None
        used_currencies = set(self._raw_cash) | {
            stock.currency for stock in self.positions + self.watchlist
        }
        forex = await self._api.get_forex_rates(self._base_currency, used_currencies)
        # convert balances
        self._raw_cash = {
            self._base_currency: sum(
                self._raw_cash[conversion_currency] / forex[conversion_currency]
                for conversion_currency in self._raw_cash
            )
        }
        # convert stocks
        for stock in self._stocks.values():
            if stock.currency is self._base_currency:
                continue
            conversion_rate = forex[stock.currency]
            stock.currency = self._base_currency
            stock.convert_currency(conversion_rate)
