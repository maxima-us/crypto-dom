import click
import pytest


@click.command()
@click.option("--signed", "-s", default=False, help="Test Private Endpoints", required=True, type=bool)
def run_tests(signed):
    # ---- Kraken Unsigned
    pytest.main(["-vv", "tests/kraken/test_kraken_response_models.py"])
    pytest.main(["-vv", "tests/kraken/test_kraken_hypothesis_market_data.py"])

    # # ---- Binance Unsigned
    pytest.main(["-vv", "tests/binance/test_binance_response_models.py"])
    pytest.main(["-vv", "tests/binance/test_binance_hypothesis_market_data.py"])

    if signed:
        # ---- Kraken Signed
        pytest.main(["-vv", "tests/binance/test_binance_hypothesis_spot_account.py"])


if __name__ == "__main__":
    run_tests()