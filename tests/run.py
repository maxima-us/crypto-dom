import sys

import pytest

if __name__ == "__main__":

    # ------ Test Binance
    # pytest.main(["-vv", "tests/binance/test_binance_response_models.py"])

    # ------ Test Kraken
    pytest.main(["-vv", "tests/kraken/test_kraken_response_models.py"])
    pytest.main(["-vv", "tests/kraken/test_kraken_hypothesis_market_data.py"])

    # ------ Test Httype Client
    # pytest.main(["-vv", "tests/test_client.py"])

