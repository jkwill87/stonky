import asyncio

from stonky.api import Api
from stonky.const import IS_DEBUG
from stonky.settings import Settings
from stonky.stock_store import StockStore
from stonky.tty import Tty, crash_report


def entrypoint():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
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
