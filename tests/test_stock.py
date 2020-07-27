from unittest import TestCase

from stonky.stock import Stock


class TestStock(TestCase):
    def test_post_init(self):
        stock = Stock(ticket="amd", currency_code="usd")
        assert stock.ticket == "AMD"
        assert stock.currency_code == "USD"

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

    def test_ticker_tape__down(self):
        stock = Stock(
            ticket="AMD",
            delta_amount=-10.123,
            delta_percent=0.156,
            volume=100.123,
            amount_bid=200.553,
        )
        assert stock.ticker_tape == "AMD     100.12  @ 200.55  ▼ -10.12 +15.60%"

    def test_ticker_tape__zero(self):
        stock = Stock(
            ticket="AMD",
            delta_amount=0.0,
            delta_percent=0.156,
            volume=100.123,
            amount_bid=200.553,
        )
        assert stock.ticker_tape == "AMD     100.12  @ 200.55  ▬  +0.00 +15.60%"

    def test_ticker_tape_up(self):
        stock = Stock(
            ticket="AMD",
            delta_amount=10.123,
            delta_percent=0.156,
            volume=100.123,
            amount_bid=200.553,
        )
        assert stock.ticker_tape == "AMD     100.12  @ 200.55  ▲ +10.12 +15.60%"

    def test_position(self):
        stock = Stock(ticket="AAPL", delta_amount=12.345, delta_percent=0.0678)
        assert stock.position == "AAPL    +12.35  +6.78%"

    def test_profit_and_loss(self):
        stock = Stock(delta_amount=12.345, delta_percent=0.0678)
        assert stock.profit_and_loss == "+6.78% +12.35 USD"
