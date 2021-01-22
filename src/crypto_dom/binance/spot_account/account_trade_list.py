import typing
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import RECV_WINDOW, SYMBOL, SYMBOL_PERMISSIONS, ASSET


# ============================================================
# ACCOUNT INFORMATION (USER DATA)
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#account-trade-list-user_data

URL = "https://api.binance.com/api/v3/myTrades"
METHOD = "GET"
WEIGHT = 5


# ------------------------------
# Sample Response (doc)
# ------------------------------


# {
#   "makerCommission": 15,
#   "takerCommission": 15,
#   "buyerCommission": 0,
#   "sellerCommission": 0,
#   "canTrade": true,
#   "canWithdraw": true,
#   "canDeposit": true,
#   "updateTime": 123456789,
#   "accountType": "SPOT",
#   "balances": [
#     {
#       "asset": "BTC",
#       "free": "4723846.89208129",
#       "locked": "0.00000000"
#     },
#     {
#       "asset": "LTC",
#       "free": "4763368.68006011",
#       "locked": "0.00000000"
#     }
#   ],
#   "permissions": [
#     "SPOT"
#   ]
# }


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint GET https://api.binance.com/api/v3/myTrades
    
    Model Fields:
    -------------
        symbol : str
        startTime : float
            Timestamp in milliseconds (optional)
        endTime : float
            Timestamp in milliseconds (optional)
        fromId : int
            TradeId to fetch from (optional)
            Default gets most recent trades
        limit : int
            Default = 500 ; Max = 1000 (optional)
        timestamp : float
        recvWindow : int
           Number of milliseconds after timestamp the request is valid for (optional)
           Default = 5000
    """
    symbol: SYMBOL
    startTime: typing.Optional[TIMESTAMP_MS]
    endTime: typing.Optional[TIMESTAMP_MS]
    fromId: typing.Optional[int]
    limit: typing.Optional[pydantic.conint(ge=0, le=1000)]

    timestamp: TIMESTAMP_MS
    recvWindow: typing.Optional[RECV_WINDOW]
    
    
# ------------------------------
# Response Model
# ------------------------------


class _Trade(pydantic.BaseModel):
    symbol: SYMBOL
    id: pydantic.PositiveInt
    orderId: pydantic.PositiveInt
    orderListId: pydantic.conint(ge=-1)
    price: Decimal
    qty: Decimal
    quoteQty: Decimal
    commission: Decimal
    commissionAsset: ASSET
    time: TIMESTAMP_MS
    isBuyer: bool
    isMaker: bool
    isBestMatch: bool



class _AccountTradeListResp(pydantic.BaseModel):
    
    # placeholder
    data: typing.Tuple[_Trade, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint GET https://api.binance.com/api/v3/myTrade

    Type: array of pydantic Models

    Model Fields:
    -------------
        symbol : str
        id : int
        orderId : int
        orderListId : int
        price : Decimal 
        qty : Decimal
        quoteQty : Decimal
        commission : Decimal
        commissionAsset : Decimal
        time : float
            Timestamp in milliseconds
        isBuyer : bool
        isMaker : bool
        isBestMatch : bool
    """

    def __call__(_cls, response):
        model = _AccountTradeListResp(data=response)
        return model.data
   
    



if __name__ == "__main__":
  
    data = [
  {
    "symbol": "BNBBTC",
    "id": 28457,
    "orderId": 100234,
    "orderListId": -1,
    "price": "4.00000100",
    "qty": "12.00000000",
    "quoteQty": "48.000012",
    "commission": "10.10000000",
    "commissionAsset": "BNB",
    "time": 1499865549590,
    "isBuyer": True,
    "isMaker": False,
    "isBestMatch": True
  }
]

    model = Response()
    model(data)