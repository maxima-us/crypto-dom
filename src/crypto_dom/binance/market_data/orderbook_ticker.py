import typing
from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.binance.definitions import SYMBOL


# ============================================================
# SYMBOL ORDER BOOK TICKER 
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#symbol-order-book-ticker

URL = "https://api.binance.com/api/v3/ticker/bookTicker"
METHOD = "GET"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


# for a single symbol

# {
#   "symbol": "LTCBTC",
#   "bidPrice": "4.00000000",
#   "bidQty": "431.00000000",
#   "askPrice": "4.00000200",
#   "askQty": "9.00000000"
# }

# OR

# for multiple symbols

# [
#   {
#     "symbol": "LTCBTC",
#     "bidPrice": "4.00000000",
#     "bidQty": "431.00000000",
#     "askPrice": "4.00000200",
#     "askQty": "9.00000000"
#   },
#   {
#     "symbol": "ETHBTC",
#     "bidPrice": "0.07946700",
#     "bidQty": "9.00000000",
#     "askPrice": "100000.00000000",
#     "askQty": "1000.00000000"
#   }
# ]


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint https://api.binance.com/api/v3/ticker/bookTicker

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


class _OrderBookTicker(pydantic.BaseModel):
    
    symbol: SYMBOL
    bidPrice: Decimal
    bidQty: Decimal
    askPrice: Decimal
    askQty: Decimal


class _OrderBookTickers(pydantic.BaseModel):

    data: typing.Tuple[_OrderBookTicker, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint https://api.binance.com/api/v3/ticker/bookTicker

    Type: pydantic.BaseModel or array of pydantic Models
    
    Model Fields:
    -------------
        symbol : str 
        bidPrice : Decimal
        bidQty : Decimal
        askPrice : Decimal
        askQty : Decimal
    """

    def __call__(self, response):

        if isinstance(response, list):
            _valid = _OrderBookTickers(data=response)
            return _valid.data
        
        if isinstance(response, dict):
            _valid = _OrderBookTicker(**response)
            return _valid
        




if __name__ == "__main__":

    data = {
  "symbol": "LTCBTC",
  "bidPrice": "4.00000000",
  "bidQty": "431.00000000",
  "askPrice": "4.00000200",
  "askQty": "9.00000000"
}

    expect = Response()
    valid = expect(data)
    print("Validated model", valid, "\n")


    data2 = [
  {
    "symbol": "LTCBTC",
    "bidPrice": "4.00000000",
    "bidQty": "431.00000000",
    "askPrice": "4.00000200",
    "askQty": "9.00000000"
  },
  {
    "symbol": "ETHBTC",
    "bidPrice": "0.07946700",
    "bidQty": "9.00000000",
    "askPrice": "100000.00000000",
    "askQty": "1000.00000000"
  }
]
    
    expect = Response()
    valid = expect(data2)
    print("Validated model", valid, "\n")



  