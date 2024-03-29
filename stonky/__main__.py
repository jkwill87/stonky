import asyncio
from sys import gettrace

from stonky.api import Api
from stonky.settings import Settings
from stonky.stock_store import StockStore
from stonky.tty import Tty, crash_report

IS_DEBUG = gettrace() is not None


def entrypoint():
    try:
        asyncio.run(main())
    except SystemExit:
        raise
    except KeyboardInterrupt:
        pass
    except:
        if IS_DEBUG:
            raise
        else:
            crash_report()


async def main():
    async with Api() as api:
        settings = Settings.load()
        stock_store = StockStore(api, settings)
        tty = Tty(settings, stock_store)
        if settings.refresh:
            await tty.draw_live()
        else:
            await tty.draw()


if __name__ == "__main__":
    entrypoint()
