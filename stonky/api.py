import asyncio
from typing import Dict, Iterable, Optional
from urllib.parse import urlencode

from aiohttp import ClientSession

from stonky.stock import Stock
from stonky.typedef import CurrencyStr


class Api:
    def __init__(self) -> None:
        self._session: Optional[ClientSession] = None

    async def __aenter__(self) -> "Api":
        self._session = ClientSession()
        return self

    async def __aexit__(self, *_) -> None:
        if self._session:
            await self._session.close()
            self._session = None

    async def get_quote(self, ticket: str) -> Stock:
        url = f"https://query1.finance.yahoo.com/v11/finance/quoteSummary/{ticket}"
        params = {"modules": "summaryDetail,price"}
        response = await self._query(url, params)
        if "error" in response:
            raise RuntimeError(f"Could not get stock information for {ticket}")
        try:
            price_data = response["quoteSummary"]["result"][0]["price"]
            stock = Stock(
                ticket=ticket,
                currency=price_data["currency"],
                current_amount=price_data["regularMarketPrice"].get("raw", 0.0),
                delta_amount=price_data["regularMarketChange"].get("raw", 0.0),
                delta_percent=price_data["regularMarketChangePercent"].get("raw", 0.0),
                market_price=price_data["regularMarketPrice"].get("raw", 0.0),
                volume=price_data["regularMarketVolume"].get("raw", 0.0),
            )
        except (TypeError, KeyError):
            raise RuntimeError(f"Could not get stock information for '{ticket}'")
        return stock

    async def get_forex_rates(
        self,
        base_currency: CurrencyStr,
        conversion_currencies: Iterable[CurrencyStr],
    ) -> Dict[CurrencyStr, float]:
        forex: Dict[CurrencyStr, float] = {base_currency: 1.0}
        futures = [
            self._set_forex_rate(base_currency, conversion_currency, forex)
            for conversion_currency in conversion_currencies
            if conversion_currency != base_currency
        ]
        await asyncio.gather(*futures)
        return forex

    async def _set_forex_rate(
        self,
        base_currency: CurrencyStr,
        conversion_currency: CurrencyStr,
        forex: Dict[CurrencyStr, float],
    ):
        url = "https://query1.finance.yahoo.com/v7/finance/spark"
        params = {
            "symbols": f"{conversion_currency}{base_currency}=X",
            "range": "1m",
        }
        response = await self._query(url, params)
        if "error" in response:
            raise RuntimeError(
                f"Cannot covert {base_currency} to {conversion_currency}"
            )
        rate = response["spark"]["result"][0]["response"][0]["meta"][
            "regularMarketPrice"
        ]
        forex[conversion_currency] = float(rate)

    async def _query(self, url: str, params: Optional[Dict] = None) -> dict:
        assert self._session is not None
        if params:
            url += "?" + urlencode(params)
        try:
            async with self._session.get(url) as response:
                return await response.json()
        except ConnectionError:
            raise RuntimeError("Network Error")
        except ValueError:
            raise RuntimeError("Could decode server response")
