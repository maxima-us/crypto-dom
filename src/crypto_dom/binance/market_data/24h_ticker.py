import typing
from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import COUNT, TIMESTAMP_MS


# ============================================================
# SYMBOL ORDER BOOK TICKER 
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#24hr-ticker-price-change-statistics

URL = "https://api.binance.com/api/v3/ticker/24hr"
METHOD = "GET"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


# for a single symbol

# {
#   "symbol": "BNBBTC",
#   "priceChange": "-94.99999800",
#   "priceChangePercent": "-95.960",
#   "weightedAvgPrice": "0.29628482",
#   "prevClosePrice": "0.10002000",
#   "lastPrice": "4.00000200",
#   "lastQty": "200.00000000",
#   "bidPrice": "4.00000000",
#   "askPrice": "4.00000200",
#   "openPrice": "99.00000000",
#   "highPrice": "100.00000000",
#   "lowPrice": "0.10000000",
#   "volume": "8913.30000000",
#   "quoteVolume": "15.30000000",
#   "openTime": 1499783499040,
#   "closeTime": 1499869899040,
#   "firstId": 28385,   // First tradeId
#   "lastId": 28460,    // Last tradeId
#   "count": 76         // Trade count
# }

# OR

# for multiple symbols

# [
#   {
#     "symbol": "BNBBTC",
#     "priceChange": "-94.99999800",
#     "priceChangePercent": "-95.960",
#     "weightedAvgPrice": "0.29628482",
#     "prevClosePrice": "0.10002000",
#     "lastPrice": "4.00000200",
#     "lastQty": "200.00000000",
#     "bidPrice": "4.00000000",
#     "askPrice": "4.00000200",
#     "openPrice": "99.00000000",
#     "highPrice": "100.00000000",
#     "lowPrice": "0.10000000",
#     "volume": "8913.30000000",
#     "quoteVolume": "15.30000000",
#     "openTime": 1499783499040,
#     "closeTime": 1499869899040,
#     "firstId": 28385,   // First tradeId
#     "lastId": 28460,    // Last tradeId
#     "count": 76         // Trade count
#   }
# ]


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint https://api.binance.com/api/v3/ticker/24hr

    Model Fields:
    -------------
        symbol : str 
            Asset pair to get price ticker data for (optional)

    Note:
    -----
        If the symbol is not sent, prices for all symbols will be returned in an array
        Careful when accessing with no symbols as weight increases from 1 to 40

    """

    symbol: typing.Optional[str] # TODO replace with PAIR


# ------------------------------
# Response Model
# ------------------------------


class _24hTicker(pydantic.BaseModel):
    
    symbol: str
    priceChange: Decimal
    priceChangePercent: Decimal
    weightedAvgPrice: Decimal
    prevClosePrice: Decimal
    lastPrice: Decimal
    lastQty: Decimal
    bidPrice: Decimal
    askPrice: Decimal
    openPrice: Decimal
    highPrice: Decimal
    lowPrice: Decimal
    volume: Decimal
    quoteVolume: Decimal
    openTime: TIMESTAMP_MS
    closeTime: TIMESTAMP_MS
    firstId: int
    lastId: int
    count: COUNT


class _24hTickers(pydantic.BaseModel):

    data: typing.Tuple[_24hTicker, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint https://api.binance.com/api/v3/ticker/24hr

    Type: pydantic.BaseModel or array of pydantic Models
    
    Model Fields:
    -------------
        symbol : str 
        priceChange : Decimal
        priceChangePercent : Decimal
        weightedAvgPrice : Decimal
        prevClosePrice : Decimal
        lastPrice : Decimal
        lastQty : Decimal
        bidPrice : Decimal
        askPrice : Decimal
        openPrice : Decimal
        highPrice : Decimal
        lowPrice : Decimal
        volume : Decimal
        quoteVolume : Decimal
        openTime : float
        closeTime : float
        firstId : int
        lastId : int
        count : int
            Number of trades
    """

    def __call__(self, response):

        if isinstance(response, list):
            _valid = _24hTickers(data=response)
            return _valid.data
        
        if isinstance(response, dict):
            _valid = _24hTicker(**response)
            return _valid
        




if __name__ == "__main__":

    data = {
  "symbol": "BNBBTC",
  "priceChange": "-94.99999800",
  "priceChangePercent": "-95.960",
  "weightedAvgPrice": "0.29628482",
  "prevClosePrice": "0.10002000",
  "lastPrice": "4.00000200",
  "lastQty": "200.00000000",
  "bidPrice": "4.00000000",
  "askPrice": "4.00000200",
  "openPrice": "99.00000000",
  "highPrice": "100.00000000",
  "lowPrice": "0.10000000",
  "volume": "8913.30000000",
  "quoteVolume": "15.30000000",
  "openTime": 1499783499040,
  "closeTime": 1499869899040,
  "firstId": 28385,
  "lastId": 28460,
  "count": 76
}

    expect = Response()
    valid = expect(data)
    print("Validated model", valid, "\n")


    data2 = [
  {
    "symbol": "BNBBTC",
    "priceChange": "-94.99999800",
    "priceChangePercent": "-95.960",
    "weightedAvgPrice": "0.29628482",
    "prevClosePrice": "0.10002000",
    "lastPrice": "4.00000200",
    "lastQty": "200.00000000",
    "bidPrice": "4.00000000",
    "askPrice": "4.00000200",
    "openPrice": "99.00000000",
    "highPrice": "100.00000000",
    "lowPrice": "0.10000000",
    "volume": "8913.30000000",
    "quoteVolume": "15.30000000",
    "openTime": 1499783499040,
    "closeTime": 1499869899040,
    "firstId": 28385,
    "lastId": 28460,
    "count": 76
  }
]
    
    expect = Response()
    valid = expect(data2)
    print("Validated model", valid, "\n")



  