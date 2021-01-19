import typing
from datetime import date
from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import COUNT, TIMESTAMP_MS
from crypto_dom.binance.definitions import TIMEFRAME


# ============================================================
# AGGREGATE TRADES
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#compressed-aggregate-trades-list

URL = "https://api.binance.com/api/v3/aggTrades"
METHOD = "GET"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


# [
#   {
#     "a": 26129,         // Aggregate tradeId
#     "p": "0.01633102",  // Price
#     "q": "4.70443515",  // Quantity
#     "f": 27781,         // First tradeId
#     "l": 27781,         // Last tradeId
#     "T": 1498793709153, // Timestamp
#     "m": true,          // Was the buyer the maker?
#     "M": true           // Was the trade the best price match?
#   }
# ]


# ------------------------------
# Request Model
# ------------------------------

class Request(pydantic.BaseModel):
    """Request model for endpoint https://api.binance.com/api/v3/aggTrades

    Model Fields:
    -------------
        symbol : str 
            Asset pair to get Trades data for
        fromId : int
            Id to get trades from (optional) 
        startTime : float
            Timestamp in milliseconds (optional)
        endTIme : float
            Timestamp in milliseconds (optional)
        limit : int
            default = 500, max = 1000 (optional)
    """

    symbol: str # TODO replace with PAIR
    fromId: typing.Optional[int]

    # timestamp in seconds
    startTime: typing.Optional[TIMESTAMP_MS]
    endTime: typing.Optional[TIMESTAMP_MS]

    limit: typing.Optional[pydantic.conint(ge=0, le=1000)]


    @pydantic.validator('startTime', allow_reuse=True)
    def check_year_from_timestamp(cls, v):
        if not v: return

        if v == 0: return v

        y = date.fromtimestamp(v).year
        if not y > 2009 and y < 2050:
            err_msg = f"Year {y} for timestamp {v} not within [2009, 2050]"
            raise ValueError(err_msg)
        return v
    
    @pydantic.validator('endTime', allow_reuse=True)
    def check_year_from_timestamp(cls, v):
        if not v: return

        if v == 0: return v

        y = date.fromtimestamp(v).year
        if not y > 2009 and y < 2050:
            err_msg = f"Year {y} for timestamp {v} not within [2009, 2050]"
            raise ValueError(err_msg)
        return v


# ------------------------------
# Response Model
# ------------------------------


class _AggTrade(pydantic.BaseModel):
    a: int
    p: Decimal
    q: Decimal
    f: int
    l: int
    T: TIMESTAMP_MS
    m: bool
    M: bool


class _AggTradesResp(pydantic.BaseModel):

    # placeholder
    data: typing.Tuple[_AggTrade, ...]


class Response:
    """Validated Response for endpoint https://api.binance.com/api/v3/aggTrades

    Type: Tuple of pydantic Models

    Model Fields:
    -------------
        ad : int
            Aggregate tradeId
        p : Decimal
            Price
        q : Decimal
            Quantity
        f : int
            First tradeId
        l : int
            Last tradeId
        T : float
            Trade executed timestamp in milliseconds
        m : bool
            Wether buyer was maker
                true = market sell
                false = market buy
        M : bool
            Wether is was the best price match
    """

    def __call__(self, response):
        # print("Calling with response", response, "`\n")
        test = _AggTradesResp(data=response)
        # print("Returning model", test, "\n")
        return test.data




if __name__ == "__main__":

    data = [
        {
            "a": 26129,
            "p": "0.01633102",
            "q": "4.70443515",
            "f": 27781,
            "l": 27781,
            "T": 1498793709153,
            "m": True,
            "M": True
        }
    ]
       

    expect = Response()
    valid = expect(data)
    print("Validated model", valid, "\n")
    # print("Data field", res.data)