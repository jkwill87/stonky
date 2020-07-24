from stonky.api import Api
from stonky.settings import Settings
from stonky.stock_store import StockStore
from stonky.tty import Tty, crash_report

from stonky.const import IS_DEBUG


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
        if IS_DEBUG:
            raise
        else:
            crash_report()


if __name__ == "__main__":
    main()
