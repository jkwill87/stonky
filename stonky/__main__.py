from asyncio import get_event_loop

from stonky.api import Api
from stonky.const import IS_DEBUG
from stonky.settings import Settings
from stonky.stock_store import StockStore
from stonky.tty import Tty, crash_report


async def main():
    try:
        async with Api() as api:
            settings = Settings()
            stock_store = StockStore(api, settings)
            await stock_store.update_stocks()
            tty = Tty(settings, stock_store)
            if settings.refresh:
                await tty.draw_live()
            else:
                await tty.draw()
    except SystemExit:
        pass
    except:
        if IS_DEBUG:
            raise
        else:
            crash_report()


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(main())
