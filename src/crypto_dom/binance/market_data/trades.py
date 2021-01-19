import typing
from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS


# ============================================================
# RECENT TRADES 
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#recent-trades-list

URL = "https://api.binance.com/api/v3/trades"
METHOD = "GET"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


# [
#   {
#     "id": 28457,
#     "price": "4.00000100",
#     "qty": "12.00000000",
#     "quoteQty": "48.000012",
#     "time": 1499865549590,
#     "isBuyerMaker": true,
#     "isBestMatch": true
#   }
# ]


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint https://api.binance.com/api/v3/trades

    Model Fields:
    -------------
        symbol : str 
            Asset pair to get OHLC data for
        limit : int
            default = 500, max = 1000 (optional)
    """

    symbol: str # TODO replace with PAIR
    limit: typing.Optional[pydantic.conint(ge=0, le=1000)]


# ------------------------------
# Response Model
# ------------------------------


class _Trade(pydantic.BaseModel):
    id: int
    price: Decimal
    qty: Decimal
    quoteQty: Decimal
    time: TIMESTAMP_MS
    isBuyerMaker: bool
    isBestMatch: bool


class _TradesResp(pydantic.BaseModel):
    
    # placeholder
    data: typing.Tuple[_Trade, ...]


class Response:
    """Validated Response for endpoint https://api.binance.com/api/v3/trades

    Type: Tuple of pydantic Models

    Model Fields:
    -------------
        id : int
            Id of trade
        price : Decimal
        qty : Decimal
        quoteQty : Decimal
        time : float
            Trade executed timestamp in milliseconds
        isBuyerMaker : bool
            true = market sell
            false = market buy
        isBestMatch : bool
    """

    def __call__(self, response):
        _valid = _TradesResp(data=response)
        return _valid.data




# ------------------------------
# Test
# ------------------------------


if __name__ == "__main__":

    data = [
  {
    "id": 28457,
    "price": "4.00000100",
    "qty": "12.00000000",
    "quoteQty": "48.000012",
    "time": 1499865549590,
    "isBuyerMaker": True,
    "isBestMatch": True
  }
]

    expect = Response()
    valid = expect(data)
    print("Validated model", valid, "\n")