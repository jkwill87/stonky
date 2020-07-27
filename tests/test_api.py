from unittest import IsolatedAsyncioTestCase

from stonky.api import Api


class TestApi(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.api = await Api().__aenter__()

    async def asyncTearDown(self) -> None:
        await self.api.__aexit__(None, None, None)

    async def test_get_quote__stock(self):
        await self.api.get_quote("AAPL")

    async def test_get_quote__cryptocurrency(self):
        await self.api.get_quote("BTC-USD")

    async def test_get_quote__mutual_fund(self):
        await self.api.get_quote("HBLFX")

    async def test_get_forex_rates(self):
        forex = await self.api.get_forex_rates("USD")
        assert forex.USD == 1
