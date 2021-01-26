import sys

import pytest

if __name__ == "__main__":

    # ------ Test Binance
    # print(globals())
    # for m in sys.modules:
    #     print(m)
    pytest.main(["-vv", "tests/binance/test_binance_response_models.py"])
    
    # ------ Test Kraken
    # print(globals())
    # for m in sys.modules:
    #     print(m)
    pytest.main(["-vv", "tests/kraken/test_kraken_response_models.py"])
    
    # ------ Test Httype Client
    pytest.main(["-vv", "tests/test_client.py"])
    
