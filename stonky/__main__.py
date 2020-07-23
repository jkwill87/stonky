from stonky.api import Api
from stonky.config import Config
from stonky.stock_store import StockStore
from stonky.view import View


def main():
    api = Api()
    config = Config()
    stock_store = StockStore(api, config)
    view = View(config, stock_store)
    if config.polling:
        view.draw_live()
    else:
        view.draw()


if __name__ == "__main__":
    main()
