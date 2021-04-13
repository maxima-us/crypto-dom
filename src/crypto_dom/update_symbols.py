import click
import asyncio

from crypto_dom.path import APP_PATH
from crypto_dom.kraken.__write_assets import _write_kraken_assets
from crypto_dom.kraken.__write_assetpairs import _write_kraken_pairs
from crypto_dom.binance.__write_assets import _write_binance_assets
from crypto_dom.binance.__write_symbols import _write_binance_symbols


@click.command()
def run():

    # ---- update symbols and assets
    async def update_symbols_assets():
        await _write_kraken_pairs(f"{APP_PATH}/kraken/")
        await _write_kraken_assets(f"{APP_PATH}/kraken/")
        await _write_binance_symbols(f"{APP_PATH}/binance/")
        await _write_binance_assets(f"{APP_PATH}/binance/")

    asyncio.run(update_symbols_assets())