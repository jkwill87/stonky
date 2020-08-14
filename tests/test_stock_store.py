from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from stonky.api import Api
from stonky.enums import SortType
from stonky.settings import Settings
from stonky.stock_store import StockStore
from tests import AAPL_STOCK, AMD_STOCK, SHOP_TO_STOCK, VGRO_TO_STOCK


class TestStockStore(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.api = Api()
        self.api._query = AsyncMock()
        self.settings = Settings()


class TestWatchlist(TestStockStore):
    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        self.settings.watchlist = {"AAPL", "AMD", "SHOP.TO", "VGRO.TO"}

    @property
    def stock_store(self):
        stock_store = StockStore(self.api, self.settings)
        stock_store._reset_raw_values()
        stock_store._stocks = {
            "AAPL": AAPL_STOCK,
            "AMD": AMD_STOCK,
            "SHOP.TO": SHOP_TO_STOCK,
            "VGRO.TO": VGRO_TO_STOCK,
        }
        return stock_store

    async def test_sort_amount(self):
        self.settings.sort = SortType.AMOUNT
        assert self.stock_store.watchlist == [
            VGRO_TO_STOCK,
            AAPL_STOCK,
            AMD_STOCK,
            SHOP_TO_STOCK,
        ]

    async def test_sort_amount_desc(self):
        self.settings.sort = SortType.AMOUNT_DESC
        assert self.stock_store.watchlist == [
            SHOP_TO_STOCK,
            AMD_STOCK,
            AAPL_STOCK,
            VGRO_TO_STOCK,
        ]

    async def test_sort_ticket(self):
        self.settings.sort = SortType.TICKET
        assert self.stock_store.watchlist == [
            AAPL_STOCK,
            AMD_STOCK,
            SHOP_TO_STOCK,
            VGRO_TO_STOCK,
        ]

    async def test_sort_ticket_desc(self):
        self.settings.sort = SortType.TICKET_DESC
        assert self.stock_store.watchlist == [
            VGRO_TO_STOCK,
            SHOP_TO_STOCK,
            AMD_STOCK,
            AAPL_STOCK,
        ]

    async def test_sort_low(self):
        self.settings.sort = SortType.LOW
        assert self.stock_store.watchlist == [
            VGRO_TO_STOCK,
            AAPL_STOCK,
            AMD_STOCK,
            SHOP_TO_STOCK,
        ]

    async def test_sort_low_desc(self):
        self.settings.sort = SortType.LOW_DESC
        assert self.stock_store.watchlist == [
            SHOP_TO_STOCK,
            AMD_STOCK,
            AAPL_STOCK,
            VGRO_TO_STOCK,
        ]

    async def test_sort_high(self):
        self.settings.sort = SortType.HIGH
        assert self.stock_store.watchlist == [
            VGRO_TO_STOCK,
            AAPL_STOCK,
            AMD_STOCK,
            SHOP_TO_STOCK,
        ]

    async def test_sort_high_desc(self):
        self.settings.sort = SortType.HIGH_DESC
        assert self.stock_store.watchlist == [
            SHOP_TO_STOCK,
            AMD_STOCK,
            AAPL_STOCK,
            VGRO_TO_STOCK,
        ]

    async def test_sort_close(self):
        self.settings.sort = SortType.CLOSE
        assert self.stock_store.watchlist == [
            VGRO_TO_STOCK,
            AAPL_STOCK,
            AMD_STOCK,
            SHOP_TO_STOCK,
        ]

    async def test_sort_close_desc(self):
        self.settings.sort = SortType.CLOSE_DESC
        assert self.stock_store.watchlist == [
            SHOP_TO_STOCK,
            AMD_STOCK,
            AAPL_STOCK,
            VGRO_TO_STOCK,
        ]

    async def test_sort_change(self):
        self.settings.sort = SortType.CHANGE
        assert self.stock_store.watchlist == [
            AAPL_STOCK,
            VGRO_TO_STOCK,
            SHOP_TO_STOCK,
            AMD_STOCK,
        ]

    async def test_sort_change_desc(self):
        self.settings.sort = SortType.CHANGE_DESC
        assert self.stock_store.watchlist == [
            AMD_STOCK,
            SHOP_TO_STOCK,
            VGRO_TO_STOCK,
            AAPL_STOCK,
        ]

    async def test_sort_volume(self):
        self.settings.sort = SortType.VOLUME
        assert self.stock_store.watchlist == [
            VGRO_TO_STOCK,
            SHOP_TO_STOCK,
            AMD_STOCK,
            AAPL_STOCK,
        ]

    async def test_sort_volume_desc(self):
        self.settings.sort = SortType.VOLUME_DESC
        assert self.stock_store.watchlist == [
            AAPL_STOCK,
            AMD_STOCK,
            SHOP_TO_STOCK,
            VGRO_TO_STOCK,
        ]
