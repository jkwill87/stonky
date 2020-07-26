from stonky.api import Api


def test_get_quote__stock():
    Api().get_quote("AAPL")


def test_get_quote__cryptocurrency():
    Api().get_quote("BTC-USD")


def test_get_quote__mutual_fund():
    Api().get_quote("HBLFX")


def test_get_forex_rates():
    forex = Api().get_forex_rates("USD")
    assert forex.USD == 1
