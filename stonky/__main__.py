from stonky.api import Api
from stonky.cli import Cli
from stonky.config import Config
from stonky.stock_store import StockStore


def main():
    api = Api()
    config = Config()
    stock_store = StockStore(api, config)
    cli = Cli(config, stock_store)
    if config.refresh:
        cli.draw_live()
    else:
        cli.draw()


if __name__ == "__main__":
    main()
