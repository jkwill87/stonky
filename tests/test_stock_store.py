from unittest import TestCase
from unittest.mock import Mock

from stonky.api import Api
from stonky.enums import SortType
from stonky.settings import Settings
from stonky.stock_store import StockStore
from tests import AAPL_STOCK, AMD_STOCK, SHOP_TO_STOCK, VGRO_TO_STOCK


class TestStockStore(TestCase):
    def setUp(self) -> None:
        self.api = Api()
        self.api._query = Mock()
        self.settings = Settings(
            positions={"AAPL": 1, "AMD": 10, "SHOP.TO": 100, "VGRO.TO": 1000,},
            watchlist=["AAPL", "AMD", "SHOP.TO", "VGRO.TO"],
        )

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


class TestWatchlist(TestStockStore):
    @property
    def watch_tickets(self):
        return [stock.ticket for stock in self.stock_store.watchlist]

    def test_sort__none(self):
        self.settings.sort = None
        assert self.watch_tickets == [
            "AAPL",
            "AMD",
            "SHOP.TO",
            "VGRO.TO",
        ]

    def test_sort__amount(self):
        self.settings.sort = SortType.AMOUNT
        assert self.watch_tickets == [
            "VGRO.TO",
            "AAPL",
            "AMD",
            "SHOP.TO",
        ]

    def test_sort__amount_desc(self):
        self.settings.sort = SortType.AMOUNT_DESC
        assert self.watch_tickets == [
            "SHOP.TO",
            "AMD",
            "AAPL",
            "VGRO.TO",
        ]

    def test_sort__ticket(self):
        self.settings.sort = SortType.TICKET
        assert self.watch_tickets == [
            "AAPL",
            "AMD",
            "SHOP.TO",
            "VGRO.TO",
        ]

    def test_sort__ticket_desc(self):
        self.settings.sort = SortType.TICKET_DESC
        assert self.watch_tickets == [
            "VGRO.TO",
            "SHOP.TO",
            "AMD",
            "AAPL",
        ]

    def test_sort__low(self):
        self.settings.sort = SortType.LOW
        assert self.watch_tickets == [
            "VGRO.TO",
            "AAPL",
            "AMD",
            "SHOP.TO",
        ]

    def test_sort__low_desc(self):
        self.settings.sort = SortType.LOW_DESC
        assert self.watch_tickets == [
            "SHOP.TO",
            "AMD",
            "AAPL",
            "VGRO.TO",
        ]

    def test_sort__high(self):
        self.settings.sort = SortType.HIGH
        assert self.watch_tickets == [
            "VGRO.TO",
            "AAPL",
            "AMD",
            "SHOP.TO",
        ]

    def test_sort__high_desc(self):
        self.settings.sort = SortType.HIGH_DESC
        assert self.watch_tickets == [
            "SHOP.TO",
            "AMD",
            "AAPL",
            "VGRO.TO",
        ]

    def test_sort__close(self):
        self.settings.sort = SortType.CLOSE
        assert self.watch_tickets == [
            "VGRO.TO",
            "AAPL",
            "AMD",
            "SHOP.TO",
        ]

    def test_sort__close_desc(self):
        self.settings.sort = SortType.CLOSE_DESC
        assert self.watch_tickets == [
            "SHOP.TO",
            "AMD",
            "AAPL",
            "VGRO.TO",
        ]

    def test_sort__change(self):
        self.settings.sort = SortType.CHANGE
        assert self.watch_tickets == [
            "AAPL",
            "VGRO.TO",
            "SHOP.TO",
            "AMD",
        ]

    def test_sort__change_desc(self):
        self.settings.sort = SortType.CHANGE_DESC
        assert self.watch_tickets == [
            "AMD",
            "SHOP.TO",
            "VGRO.TO",
            "AAPL",
        ]

    def test_sort__volume(self):
        self.settings.sort = SortType.VOLUME
        assert self.watch_tickets == [
            "VGRO.TO",
            "SHOP.TO",
            "AMD",
            "AAPL",
        ]

    def test_sort__volume_desc(self):
        self.settings.sort = SortType.VOLUME_DESC
        assert self.watch_tickets == [
            "AAPL",
            "AMD",
            "SHOP.TO",
            "VGRO.TO",
        ]


class TestPositions(TestStockStore):
    @property
    def position_tickets(self):
        return [stock.ticket for stock in self.stock_store.positions]

    def test_sort__none(self):
        self.settings.sort = None
        assert self.position_tickets == [
            "AAPL",
            "AMD",
            "SHOP.TO",
            "VGRO.TO",
        ]

    def test_sort__amount(self):
        self.settings.sort = SortType.AMOUNT
        assert self.position_tickets == ["VGRO.TO", "AAPL", "AMD", "SHOP.TO"]

    def test_sort__amount_desc(self):
        self.settings.sort = SortType.AMOUNT_DESC
        assert self.position_tickets == ["SHOP.TO", "AMD", "AAPL", "VGRO.TO"]

    def test_sort__ticket(self):
        self.settings.sort = SortType.TICKET
        assert self.position_tickets == ["AAPL", "AMD", "SHOP.TO", "VGRO.TO"]

    def test_sort__ticket_desc(self):
        self.settings.sort = SortType.TICKET_DESC
        assert self.position_tickets == ["VGRO.TO", "SHOP.TO", "AMD", "AAPL"]

    def test_sort__low(self):
        self.settings.sort = SortType.LOW
        assert self.position_tickets == ["VGRO.TO", "AAPL", "AMD", "SHOP.TO"]

    def test_sort__low_desc(self):
        self.settings.sort = SortType.LOW_DESC
        assert self.position_tickets == ["SHOP.TO", "AMD", "AAPL", "VGRO.TO"]

    def test_sort__high(self):
        self.settings.sort = SortType.HIGH
        assert self.position_tickets == ["VGRO.TO", "AAPL", "AMD", "SHOP.TO"]

    def test_sort__high_desc(self):
        self.settings.sort = SortType.HIGH_DESC
        assert self.position_tickets == ["SHOP.TO", "AMD", "AAPL", "VGRO.TO"]

    def test_sort__close(self):
        self.settings.sort = SortType.CLOSE
        assert self.position_tickets == ["AAPL", "AMD", "VGRO.TO", "SHOP.TO"]

    def test_sort__close_desc(self):
        self.settings.sort = SortType.CLOSE_DESC
        assert self.position_tickets == ["SHOP.TO", "VGRO.TO", "AMD", "AAPL"]

    def test_sort__change(self):
        self.settings.sort = SortType.CHANGE
        assert self.position_tickets == ["AAPL", "VGRO.TO", "SHOP.TO", "AMD"]

    def test_sort__change_desc(self):
        self.settings.sort = SortType.CHANGE_DESC
        assert self.position_tickets == ["AMD", "SHOP.TO", "VGRO.TO", "AAPL"]

    def test_sort__volume(self):
        self.settings.sort = SortType.VOLUME
        assert self.position_tickets == ["VGRO.TO", "SHOP.TO", "AMD", "AAPL"]

    def test_sort__volume_desc(self):
        self.settings.sort = SortType.VOLUME_DESC
        assert self.position_tickets == ["AAPL", "AMD", "SHOP.TO", "VGRO.TO"]
