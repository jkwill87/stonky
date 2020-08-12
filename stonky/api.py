import asyncio
from typing import Dict, Optional, Set
from urllib.parse import urlencode

from aiohttp import ClientSession

from stonky.enums import CurrencyType
from stonky.exceptions import StonkyException
from stonky.stock import Stock


class Api:
    def __init__(self):
        self._session: Optional[ClientSession] = None

    async def __aenter__(self):
        self._session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()
            self._session = None

    async def get_quote(self, ticket: str) -> Stock:
        url = f"https://query1.finance.yahoo.com/v11/finance/quoteSummary/{ticket}"
        params = {"modules": "summaryDetail,price"}
        response = await self._query(url, params)
        if "error" in response:
            raise StonkyException(
                f"Could not get stock information for {ticket}"
            )
        try:
            summary_data = response["quoteSummary"]["result"][0][
                "summaryDetail"
            ]
            price_data = response["quoteSummary"]["result"][0]["price"]
            stock = Stock(
                ticket=ticket,
                currency=CurrencyType(price_data["currency"]),
                amount_bid=summary_data["bid"].get("raw", 0.0),
                amount_ask=summary_data["ask"].get("raw", 0.0),
                amount_low=summary_data["dayLow"].get("raw", 0.0),
                amount_high=summary_data["dayHigh"].get("raw", 0.0),
                amount_prev_close=summary_data["previousClose"].get("raw", 0.0),
                delta_amount=price_data["regularMarketChange"].get("raw", 0.0),
                delta_percent=price_data["regularMarketChangePercent"].get(
                    "raw", 0.0
                ),
                market_price=price_data["regularMarketPrice"].get("raw", 0.0),
                volume=summary_data["volume"].get("raw", 0.0),
            )
        except TypeError:
            raise StonkyException(
                f"Could not get stock information for '{ticket}'"
            )
        return stock

    async def get_forex_rates(
        self,
        base_currency: CurrencyType,
        currency_filter: Set[CurrencyType] = None,
    ):
        forex = {base_currency: 1.0}
        futures = [
            self._set_forex_rate(base_currency, conversion_currency, forex)
            for conversion_currency in (currency_filter or set(CurrencyType))
            if conversion_currency != base_currency
        ]
        await asyncio.gather(*futures)
        return forex

    async def _set_forex_rate(
        self,
        base_currency: CurrencyType,
        conversion_currency: CurrencyType,
        forex: Dict[CurrencyType, float],
    ):
        url = "https://query1.finance.yahoo.com/v7/finance/spark"
        params = {
            "symbols": f"{conversion_currency.value}{base_currency.value}=X",
            "range": "1m",
        }
        response = await self._query(url, params)
        if "error" in response:
            raise StonkyException(
                f"Cannot covert {base_currency.value} to {conversion_currency.value}"
            )
        rate = response["spark"]["result"][0]["response"][0]["meta"][
            "regularMarketPrice"
        ]
        forex[conversion_currency] = rate

    async def _query(self, url: str, params: dict = None) -> dict:
        if params:
            url += "?" + urlencode(params)
        try:
            async with self._session.get(url) as response:
                return await response.json()
        except ConnectionError:
            raise StonkyException("Network Error")
        except ValueError:
            raise StonkyException("Could decode server response")
