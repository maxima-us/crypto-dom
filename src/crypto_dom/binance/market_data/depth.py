import typing
from decimal import Decimal

import pydantic
import stackprinter
from typing_extensions import Literal
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.binance.definitions import TIMEFRAME, SYMBOL


# ============================================================
# DEPTH (ORDERBOOK)
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#order-book 

URL = "https://api.binance.com/api/v3/depth"
METHOD = "GET"
WEIGHT = None   # adjusted based on the limit, from 1 to 50


# ------------------------------
# Sample Response (doc)
# ------------------------------


# {
#   "lastUpdateId": 1027024,
#   "bids": [
#     [
#       "4.00000000",     // PRICE
#       "431.00000000"    // QTY
#     ]
#   ],
#   "asks": [
#     [
#       "4.00000200",
#       "12.00000000"
#     ]
#   ]
# }


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint https://api.binance.com/api/v3/depth

    Model Fields:
    -------------
        symbol : str 
            Asset pair to get OHLC data for
        limit : int
            Default 100; max 5000. Valid limits:[5, 10, 20, 50, 100, 500, 1000, 5000]
            (Optional)
    """

    symbol: SYMBOL
    limit: typing.Optional[Literal[5, 10, 20, 50, 100, 500, 1000, 5000]]


# ------------------------------
# Response Model
# ------------------------------


# tuple of PRICE, QTY
_bidask_level = typing.Tuple[Decimal, Decimal]


class _Depth(pydantic.BaseModel):
    
    lastUpdateId: int
    bids: typing.Tuple[_bidask_level, ...]
    asks: typing.Tuple[_bidask_level, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint https://api.binance.com/api/v3/depth

    Type: pydantic.BaseModel
    
    Model Fields:
    -------------
        lastUpdateID : int 
            Id of last update (not a timestamp)
        bids: list
            List of tuples (`price`, `qty`)
        asks: list
            List of tuples (`price`, `qty`)
    """

    def __new__(_cls):
        return _Depth
        

