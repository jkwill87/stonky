from collections.abc import Mapping
from copy import copy
from typing import List

from stonky.api import Api
from stonky.settings import Settings
from stonky.stock import Stock


class StockStore(Mapping):
    def __init__(self, api: Api, config: Settings):
        self.api = api
        self.settings = config
        self._stocks = {}
        self.update_stocks()

    def __getitem__(self, key: str):
        return self._stocks[key]

    def __iter__(self):
        return iter(self._stocks)

    def __len__(self):
        return len(self._stocks)

    def update_stocks(self):
        self._stocks = {
            ticket: self.api.get_quote(ticket)
            for ticket in self.settings.all_tickets
        }
        if self.settings.currency:
            forex = self.api.get_forex_rates(self.settings.currency)
            for stock in self._stocks.values():
                stock.convert_currency(forex, self.settings.currency)

    @property
    def watchlist(self) -> List[Stock]:
        return self._try_sort(
            [
                stock
                for ticket, stock in self.items()
                if ticket in self.settings.watchlist
            ]
        )

    @property
    def positions(self) -> List[Stock]:
        results = []
        for ticket, amount in self.settings.positions.items():
            stock = copy(self[ticket])
            stock.delta_amount *= amount
            results.append(stock)
        return self._try_sort(results)

    @property
    def profit_and_loss(self):
        pnl = {}
        for ticket, amount in self.settings.positions.items():
            stock = copy(self[ticket])
            stock.delta_amount *= amount
            stock.amount_prev_close *= amount
            if stock.currency_code not in pnl:
                pnl[stock.currency_code] = stock
            else:
                pnl[
                    stock.currency_code
                ].amount_prev_close += stock.amount_prev_close
                pnl[stock.currency_code].delta_amount += stock.delta_amount
        results = []
        for pnl_line in pnl.values():
            pnl_line.delta_percent = (
                pnl_line.delta_amount / pnl_line.amount_prev_close
            )
            results.append(pnl_line)
        return self._try_sort(results)

    @property
    def balances(self):
        balances = {}
        for ticket, amount in self.settings.positions.items():
            stock = self[ticket]
            if stock.currency_code not in balances:
                balances[stock.currency_code] = stock.amount_bid * amount
            else:
                balances[stock.currency_code] += stock.amount_bid * amount
        for currency_code, amount in self.settings.cash.items():
            currency_code = self.settings.currency or currency_code
            if currency_code not in balances:
                balances[currency_code] = amount
            else:
                balances[currency_code] += amount
        return balances

    def _try_sort(self, stocks: List[Stock]):
        if self.settings.sort:
            stocks.sort(key=lambda _: getattr(_, self.settings.sort.value))
        return stocks
