import asyncio
from copy import copy
from typing import List

from stonky.api import Api
from stonky.settings import Settings
from stonky.stock import Stock


class StockStore:
    def __init__(self, api: Api, settings: Settings):
        self._stocks = {}
        self._api = api
        self._sort = settings.sort
        self._base_currency = settings.currency
        self._settings = settings
        self._raw_cash = None
        self._raw_positions = None
        self._raw_watchlist = None
        self._raw_tickets = None

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
    def profit_and_loss(self):
        pnl = {}
        for ticket, count in self._raw_positions.items():
            stock = copy(self._stocks[ticket])
            stock.increase_count(count)
            if stock.currency not in pnl:
                pnl[stock.currency] = stock
            else:
                pnl[stock.currency].amount_prev_close += stock.amount_prev_close
                pnl[stock.currency].delta_amount += stock.delta_amount
        results = []
        for pnl_line in pnl.values():
            pnl_line.delta_percent = (
                pnl_line.delta_amount / pnl_line.amount_prev_close
            )
            results.append(pnl_line)
        return results

    @property
    def balances(self):
        balances = {}
        for ticket, count in self._raw_positions.items():
            stock = self._stocks[ticket]
            if stock.currency not in balances:
                balances[stock.currency] = stock.amount_current * count
            else:
                balances[stock.currency] += stock.amount_current * count
        for currency, amount in self._raw_cash.items():
            if currency not in balances:
                balances[currency] = amount
            else:
                balances[currency] += amount
        return balances

    def _try_sort(self, stocks: List[Stock]):
        if self._sort:
            reverse = self._sort.value.endswith("_desc")
            sort, *_ = self._sort.value.rsplit("_desc")
            stocks.sort(key=lambda _: getattr(_, sort), reverse=reverse)
        return stocks

    def _reset_raw_values(self):
        self._raw_cash = copy(self._settings.cash)
        self._raw_positions = copy(self._settings.positions)
        self._raw_watchlist = copy(self._settings.watchlist)
        self._raw_tickets = set(self._settings.positions) | set(
            self._settings.watchlist
        )

    async def _update_quotes(self):
        futures = tuple(
            self._api.get_quote(ticket) for ticket in self._raw_tickets
        )
        self._stocks = {
            stock.ticket: stock for stock in await asyncio.gather(*futures)
        }

    async def _convert_currencies(self):
        used_currencies = set(self._raw_cash) | {
            stock.currency for stock in self.positions
        }
        forex = await self._api.get_forex_rates(
            self._base_currency, used_currencies
        )
        # convert balances
        base_amount = self._raw_cash.get(self._base_currency, 0.0)
        self._raw_cash = {
            self._base_currency: base_amount
            + sum(
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
