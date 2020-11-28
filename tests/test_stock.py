from unittest import TestCase

from stonky.stock import Stock


class TestStock(TestCase):
    def test_post_init(self):
        stock = Stock(ticket="amd")
        assert stock.ticket == "AMD"

    def test_volume_str__hundreds__lower(self):
        stock = Stock(volume=0)
        assert stock.volume_str == ""

    def test_volume_str__hundreds__upper(self):
        stock = Stock(volume=999.99)
        assert stock.volume_str == "999.99"

    def test_volume_str__thousands__lower(self):
        stock = Stock(volume=1_000)
        assert stock.volume_str == "1K"

    def test_volume_str__thousands__upper(self):
        stock = Stock(volume=999_999)
        assert stock.volume_str == "999.9K"

    def test_volume_str__millions__lower(self):
        stock = Stock(volume=1_000_000)
        assert stock.volume_str == "1M"

    def test_volume_str__millions__upper(self):
        stock = Stock(volume=999_999_999)
        assert stock.volume_str == "999.9M"

    def test_voume_str__billions__lower(self):
        stock = Stock(volume=1_000_000_000)
        assert stock.volume_str == "1B"

    def test_voume_str__billions__upper(self):
        stock = Stock(volume=999_999_999_999)
        assert stock.volume_str == "999.9B"

    def test_colour__red(self):
        stock = Stock(delta_amount=-100)
        assert stock.colour == "red"

    def test_colour__yellow(self):
        stock = Stock(delta_amount=0)
        assert stock.colour == "yellow"

    def test_colour__green(self):
        stock = Stock(delta_amount=100)
        assert stock.colour == "green"
