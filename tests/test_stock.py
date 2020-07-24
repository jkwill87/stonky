from stonky.stock import Stock


def test_post_init():
    stock = Stock(ticket="amd", currency_code="usd")
    assert stock.ticket == "AMD"
    assert stock.currency_code == "USD"


def test_volume_str__hundreds__lower():
    stock = Stock(volume=0)
    assert stock.volume_str == "0.00"


def test_volume_str__hundreds__upper():
    stock = Stock(volume=999.99)
    assert stock.volume_str == "999.99"


def test_volume_str__thousands__lower():
    stock = Stock(volume=1_000)
    assert stock.volume_str == "1K"


def test_volume_str__thousands__upper():
    stock = Stock(volume=999_999)
    assert stock.volume_str == "999.9K"


def test_volume_str__millions__lower():
    stock = Stock(volume=1_000_000)
    assert stock.volume_str == "1M"


def test_volume_str__millions__upper():
    stock = Stock(volume=999_999_999)
    assert stock.volume_str == "999.9M"


def test_voume_str__billions__lower():
    stock = Stock(volume=1_000_000_000)
    assert stock.volume_str == "1B"


def test_voume_str__billions__upper():
    stock = Stock(volume=999_999_999_999)
    assert stock.volume_str == "999.9B"


def test_colour__red():
    stock = Stock(delta_amount=-100)
    assert stock.colour == "red"


def test_colour__yellow():
    stock = Stock(delta_amount=0)
    assert stock.colour == "yellow"


def test_colour__green():
    stock = Stock(delta_amount=100)
    assert stock.colour == "green"


def test_ticker_tape__down():
    stock = Stock(
        ticket="AMD",
        delta_amount=-10.123,
        delta_percent=0.156,
        volume=100.123,
        amount_bid=200.553,
    )
    assert stock.ticker_tape == "AMD     100.12  @ 200.55  ▼ -10.12 +15.60%"


def test_ticker_tape__zero():
    stock = Stock(
        ticket="AMD",
        delta_amount=0.0,
        delta_percent=0.156,
        volume=100.123,
        amount_bid=200.553,
    )
    assert stock.ticker_tape == "AMD     100.12  @ 200.55  ▬  +0.00 +15.60%"


def test_ticker_tape_up():
    stock = Stock(
        ticket="AMD",
        delta_amount=10.123,
        delta_percent=0.156,
        volume=100.123,
        amount_bid=200.553,
    )
    assert stock.ticker_tape == "AMD     100.12  @ 200.55  ▲ +10.12 +15.60%"


def test_position():
    stock = Stock(ticket="AAPL", delta_amount=12.345, delta_percent=0.0678)
    assert stock.position == "AAPL    +12.35  +6.78%"


def test_profit_and_loss():
    stock = Stock(delta_amount=12.345, delta_percent=0.0678)
    assert stock.profit_and_loss == "+6.78% +12.35 USD"
