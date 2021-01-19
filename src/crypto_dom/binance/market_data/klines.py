import typing
from datetime import date
from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_S
from crypto_dom.binance.definitions import TIMEFRAME


# ============================================================
# KLINES (OHLC)
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data

URL = "https://api.binance.com/api/v3/klines"
METHOD = "GET"


# ------------------------------
# Sample Response (doc)
# ------------------------------


# [
#   [
#     1499040000000,      // Open time
#     "0.01634790",       // Open
#     "0.80000000",       // High
#     "0.01575800",       // Low
#     "0.01577100",       // Close
#     "148976.11427815",  // Volume
#     1499644799999,      // Close time
#     "2434.19055334",    // Quote asset volume
#     308,                // Number of trades
#     "1756.87402397",    // Taker buy base asset volume
#     "28.46694368",      // Taker buy quote asset volume
#     "17928899.62484339" // Ignore.
#   ]
# ]


# ------------------------------
# Request Model
# ------------------------------

class Request(pydantic.BaseModel):
    """Request model for endpoint https://api.binance.com/api/v3/klines

    Model Fields:
    -------
        symbol : str 
            Asset pair to get OHLC data for
        interval : int 
            Time frame interval in minutes (optional)
        startTime : float
            Timestamp (optional)
        endTIme: float
            Timestamp (optional)
        limit: int
            default = 500, max = 1000 (optional)
    """

    symbol: str # TODO replace with PAIR
    interval: typing.Optional[TIMEFRAME]

    # timestamp in seconds
    startTime: typing.Optional[TIMESTAMP_S]
    endTime: typing.Optional[TIMESTAMP_S]

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


    #! Impossible to define a model for this
    #! Begs the question if we should just define types for the result instead of models, and then pass it to ExchangeRsponse
    #! But even that might not do it, as expected response here is the following:

    #! if error: {"code": -1121, "msg": "Invalid symbol"}
    #! if success: a tuple (see below) without any index

    #! POSSIBLE SOLUTION : use a placeholder ?


_Candle = typing.Tuple[
        int, #open time
        Decimal, Decimal, Decimal, Decimal, # open high low close
        Decimal, #volume
        int, #close time
        Decimal, #asset volume
        int, #number of trades
        Decimal, #taker buy base asset volume
        Decimal, #taker buy quote asset volume
        Decimal, #ignore
    ]


class _KlinesResp(pydantic.BaseModel):
    

    # placeholder
    data: typing.Tuple[_Candle, ...]


class Response:

    def __call__(self, response):
        # print("Calling with response", response, "`\n")
        test = _KlinesResp(data=response)
        # print("Returning model", test, "\n")
        return test.data




if __name__ == "__main__":

    data = [
        [
            1499040000000,
            "0.01634790",
            "0.80000000",
            "0.01575800",
            "0.01577100",
            "148976.11427815",
            1499644799999,
            "2434.19055334",
            308,
            "1756.87402397",
            "28.46694368",
            "17928899.62484339"
        ]
    ]

    expect = Response()
    valid = expect(data)
    print("Validated model", valid, "\n")
    # print("Data field", res.data)