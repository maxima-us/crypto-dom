import click
import pytest
import asyncio

from crypto_dom.path import APP_PATH
from crypto_dom.kraken.__write_assets import _write_kraken_assets
from crypto_dom.kraken.__write_assetpairs import _write_kraken_pairs
from crypto_dom.binance.__write_assets import _write_binance_assets
from crypto_dom.binance.__write_symbols import _write_binance_symbols


@click.command()
@click.option("--signed", "-s", default=False, help="Test Private Endpoints", required=True, type=bool)
def run_tests(signed):

    # ---- update symbols and assets
    async def update_symbols_assets():
        await _write_kraken_pairs(f"{APP_PATH}/kraken/")
        await _write_kraken_assets(f"{APP_PATH}/kraken/")
        await _write_binance_symbols(f"{APP_PATH}/binance/")
        await _write_binance_assets(f"{APP_PATH}/binance/")

    asyncio.run(update_symbols_assets())

    # ---- Kraken Unsigned
    pytest.main(["-vv", "tests/kraken/test_kraken_response_models.py"])
    pytest.main(["-vv", "tests/kraken/test_kraken_hypothesis_market_data.py"])
    
    if signed:
        # ---- Kraken Signed
        pytest.main(["-vv", "tests/kraken/test_binance_hypothesis_user_data.py"])

    # # ---- Binance Unsigned
    pytest.main(["-vv", "tests/binance/test_binance_response_models.py"])
    pytest.main(["-vv", "tests/binance/test_binance_hypothesis_market_data.py"])

    if signed:
        # ---- Binance Signed
        pytest.main(["-vv", "tests/binance/test_binance_hypothesis_spot_account.py"])


if __name__ == "__main__":
    run_tests()