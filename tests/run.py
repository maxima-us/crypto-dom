import pytest

if __name__ == "__main__":
    print(globals())
    pytest.main(["-vv", "tests/binance/test_binance_response_models.py"])
    print(globals())
    pytest.main(["-vv", "tests/kraken/test_kraken_response_models.py"])