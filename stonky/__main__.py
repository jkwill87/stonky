from stonky.api import Api
from stonky.settings import Settings
from stonky.stock_store import StockStore
from stonky.tty import Tty


def main():
    api = Api()
    settings = Settings()
    stock_store = StockStore(api, settings)
    tty = Cli(settings, stock_store)
    if settings.refresh:
        tty.draw_live()
    else:
        tty.draw()


if __name__ == "__main__":
    main()
