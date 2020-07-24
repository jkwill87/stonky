from stonky.api import Api


def test_get_quote():
    Api().get_quote("AAPL")


def test_get_forex_rates():
    forex = Api().get_forex_rates("USD")
    assert forex.USD == 1
