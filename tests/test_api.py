from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from stonky.api import Api
from stonky.enums import CurrencyType
from tests.fixtures import (
    AAPL_RESPONSE,
    BTC_RESPONSE,
    CAD_USD_REPONSE,
    HBLFX_RESPONSE,
)


class TestApi(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.api = await Api().__aenter__()

    async def asyncTearDown(self) -> None:
        await self.api.__aexit__(None, None, None)

    async def test_get_quote__stock(self):
        self.api._query = AsyncMock(return_value=AAPL_RESPONSE)
        stock = await self.api.get_quote("AAPL")
        assert stock.ticket == "AAPL"
        assert stock.currency == CurrencyType.USD
        assert stock.amount_bid == 452.49
        assert stock.amount_ask == 452.67
        assert stock.amount_low == 441.19
        assert stock.amount_high == 453.1
        assert stock.amount_prev_close == 437.5
        assert stock.delta_amount == 14.540009
        assert stock.delta_percent == 0.033234306
        assert stock.market_price == 452.04
        assert stock.volume == 41486205

    async def test_get_quote__cryptocurrency(self):
        self.api._query = AsyncMock(return_value=BTC_RESPONSE)
        stock = await self.api.get_quote("BTC-USD")
        assert stock.ticket == "BTC-USD"
        assert stock.currency == CurrencyType.USD
        assert stock.amount_bid == 0.0
        assert stock.amount_ask == 0.0
        assert stock.amount_low == 11568.912
        assert stock.amount_high == 11649.112
        assert stock.amount_prev_close == 11583.987
        assert stock.delta_amount == 0.69628906
        assert stock.delta_percent == 6.0107894e-05
        assert stock.market_price == 11584.684
        assert stock.volume == 24981215232

    async def test_get_quote__mutual_fund(self):
        self.api._query = AsyncMock(return_value=HBLFX_RESPONSE)
        stock = await self.api.get_quote("HBLFX")
        assert stock.ticket == "HBLFX"
        assert stock.currency == CurrencyType.USD
        assert stock.amount_bid == 0.0
        assert stock.amount_ask == 0.0
        assert stock.amount_low == 0.0
        assert stock.amount_high == 0.0
        assert stock.amount_prev_close == 15.04
        assert stock.delta_amount == 0.04
        assert stock.delta_percent == 0.0026595744
        assert stock.market_price == 15.08
        assert stock.volume == 0.0

    async def test_get_forex_rates(self):
        self.api._query = AsyncMock(return_value=CAD_USD_REPONSE)
        forex = await self.api.get_forex_rates(
            CurrencyType.USD, {CurrencyType.CAD}
        )
        self.api._query.assert_called_once()
        assert forex[CurrencyType.USD] == 1.0
        assert forex[CurrencyType.CAD] == 0.7555
