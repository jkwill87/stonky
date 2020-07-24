import json
from urllib.parse import urlencode
from urllib.request import urlopen

from stonky.forex import Forex
from stonky.stock import Stock


class Api:
    def get_quote(self, ticket: str) -> Stock:
        url = f"https://query1.finance.yahoo.com/v11/finance/quoteSummary/{ticket}"
        params = {"modules": "summaryDetail,price"}
        response = self._query(url, params)
        summary_data = response["quoteSummary"]["result"][0]["summaryDetail"]
        price_data = response["quoteSummary"]["result"][0]["price"]
        return Stock(
            ticket=ticket,
            currency_code=price_data["currency"],
            amount_bid=summary_data["bid"].get("raw", 0.0),
            amount_ask=summary_data["ask"].get("raw", 0.0),
            amount_low=summary_data["dayLow"].get("raw", 0.0),
            amount_high=summary_data["dayHigh"].get("raw", 0.0),
            amount_prev_close=summary_data["previousClose"].get("raw", 0.0),
            delta_amount=price_data["regularMarketChange"].get("raw", 0.0),
            delta_percent=price_data["regularMarketChangePercent"].get(
                "raw", 0.0
            ),
            volume=summary_data["volume"]["raw"],
        )

    def get_forex_rates(self, base: str) -> Forex:
        url = "https://api.exchangeratesapi.io/latest"
        params = {"base": base}
        response = self._query(url, params)
        return Forex(**response["rates"])

    @staticmethod
    def _query(url: str, params: dict) -> dict:
        if params:
            url += "?" + urlencode(params)
        response = urlopen(url)
        return json.loads(response.read())
