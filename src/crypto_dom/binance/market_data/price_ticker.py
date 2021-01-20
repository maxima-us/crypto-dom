import typing
from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.binance.definitions import SYMBOL


# ============================================================
# SYMBOL PRICE TICKER 
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#symbol-price-ticker

URL = "https://api.binance.com/api/v3/ticker/price"
METHOD = "GET"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


# for a single symbol

# {
#   "symbol": "LTCBTC",
#   "price": "4.00000200"
# }

# OR

# for multiple symbols

# [
#   {
#     "symbol": "LTCBTC",
#     "price": "4.00000200"
#   },
#   {
#     "symbol": "ETHBTC",
#     "price": "0.07946600"
#   }
# ]


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint https://api.binance.com/api/v3/ticker/price

    Model Fields:
    -------------
        symbol : str 
            Asset pair to get price ticker data for (optional)

    Note:
    -----
        If the symbol is not sent, prices for all symbols will be returned in an array

    """

    symbol: typing.Optional[SYMBOL] # TODO replace with PAIR


# ------------------------------
# Response Model
# ------------------------------


class _PriceTicker(pydantic.BaseModel):
    
    symbol: SYMBOL
    price: Decimal


class _PriceTickers(pydantic.BaseModel):

    data: typing.Tuple[_PriceTicker, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint https://api.binance.com/api/v3/ticker/price

    Type: pydantic.BaseModel or array of pydantic Models
    
    Model Fields:
    -------------
        symbol : str 
        price : Decimal
    """

    def __call__(self, response):

        if isinstance(response, list):
            _valid = _PriceTickers(data=response)
            return _valid.data
        
        if isinstance(response, dict):
            _valid = _PriceTicker(**response)
            return _valid
        




if __name__ == "__main__":

    data = {
        "symbol": "LTCBTC",
        "price": "4.00000200"
    }

    expect = Response()
    valid = expect(data)
    print("Validated model", valid, "\n")


    data2 = [
        {
            "symbol": "LTCBTC",
            "price": "4.00000200"
        },
        {
            "symbol": "ETHBTC",
            "price": "0.07946600"
        }
    ]
    
    expect = Response()
    valid = expect(data2)
    print("Validated model", valid, "\n")