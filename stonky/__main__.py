from stonky.api import Api
from stonky.cli import Cli
from stonky.settings import Settings
from stonky.stock_store import StockStore


def main():
    api = Api()
    settings = Settings()
    stock_store = StockStore(api, settings)
    cli = Cli(settings, stock_store)
    if settings.refresh:
        cli.draw_live()
    else:
        cli.draw()


if __name__ == "__main__":
    main()
