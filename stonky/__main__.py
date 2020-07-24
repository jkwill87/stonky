from stonky.api import Api
from stonky.settings import Settings
from stonky.stock_store import StockStore
from stonky.tty import Tty, crash_report


def main():
    try:
        api = Api()
        settings = Settings()
        stock_store = StockStore(api, settings)
        tty = Tty(settings, stock_store)
        if settings.refresh:
            tty.draw_live()
        else:
            tty.draw()
    except:
        crash_report()


if __name__ == "__main__":
    main()
