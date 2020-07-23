from stonky.api import Api
from stonky.config import Config
from stonky.stock_store import StockStore
from stonky.view import View


def main():
    api = Api()
    config = Config()
    stock_store = StockStore(api, config)

    view = View(config, stock_store)

    if config.watchlist:
        print(view.watchlist)

    if config.positions:
        print()
        print(view.positions)
        print()
        print(view.profit_and_loss)
        print()
        print(view.balances_str)


if __name__ == "__main__":
    main()
