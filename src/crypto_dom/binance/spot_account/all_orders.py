import typing
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import  ORDER_SIDE, ORDER_STATUS, ORDER_TYPE, ORDER_TIF, RECV_WINDOW, SYMBOL


# ============================================================
# ALL ORDERS (USER DATA)
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#all-orders-user_data

URL = "https://api.binance.com/api/v3/allOrders"
METHOD = "GET"
WEIGHT = 5  # 40 if symbol parameter is ommited


# ------------------------------
# Sample Response (doc)
# ------------------------------


# [
#   {
#     "symbol": "LTCBTC",
#     "orderId": 1,
#     "orderListId": -1, //Unless OCO, the value will always be -1
#     "clientOrderId": "myOrder1",
#     "price": "0.1",
#     "origQty": "1.0",
#     "executedQty": "0.0",
#     "cummulativeQuoteQty": "0.0",
#     "status": "NEW",
#     "timeInForce": "GTC",
#     "type": "LIMIT",
#     "side": "BUY",
#     "stopPrice": "0.0",
#     "icebergQty": "0.0",
#     "time": 1499827319559,
#     "updateTime": 1499827319559,
#     "isWorking": true,
#     "origQuoteOrderQty": "0.000000"
#   }
# ]


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint GET https://api.binance.com/api/v3/allOrders

    Model Fields:
    -------------
        symbol : str
        orderId: int
            (optional)
        startTime: float
            Timestamp in milliseconds (optional)
        endTime: float
            Timestamp in milliseconds (optional)
        limit: int
            Default = 500, Max = 1000 (optional)
        timestamp : float
            Timestamp in millisecond
        recvWindow : int
           Number of milliseconds after timestamp the request is valid for (optional)
           Default = 5000

    """

    symbol: SYMBOL
    orderId: typing.Optional[pydantic.PositiveInt]
    startTime: typing.Optional[TIMESTAMP_MS]
    endTime: typing.Optional[TIMESTAMP_MS]
    limit: typing.Optional[pydantic.conint(ge=0, le=1000)]

    timestamp: TIMESTAMP_MS
    recvWindow: typing.Optional[RECV_WINDOW]


# ------------------------------
# Response Model
# ------------------------------


class _Order(pydantic.BaseModel):

    symbol: SYMBOL
    orderId: pydantic.PositiveInt
    orderListId: pydantic.conint(ge=-1)
    clientOrderId: str
    price: Decimal
    origQty: Decimal
    executedQty: Decimal
    cummulativeQuoteQty: Decimal
    status: ORDER_STATUS
    timeInForce: ORDER_TIF
    type: ORDER_TYPE
    side: ORDER_SIDE
    stopPrice: typing.Optional[Decimal]
    icebergQty: Decimal
    time: TIMESTAMP_MS
    updateTime: TIMESTAMP_MS
    isWorking: bool
    origQuoteOrderQty: Decimal


class _AllOrdersResp(pydantic.BaseModel):
    
    data: typing.Tuple[_Order, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint GET https://api.binance.com/api/v3/allOrders

    Type: Tuple of pydantic.BaseModel

    Model Fields:
    -------------
        symbol: str
        orderId: int
        orderListId: int
        clientOrderId: str
        price: Decimal
        origQty: Decimal
        executedQty: Decimal
        cummulativeQuoteQty: Decimal
        status: str enum
        timeInForce: str enum
        type: str enum
        side: str enum
        stopPrice: Decimal
            (optional)
        icebergQty: Decimal
        time: float
            Timestamp in milliseconds
        updateTime: float
            Timestamp in milliseconds
        isWorking: bool
        origQuoteOrderQty: Decimal
    """

    def __call__(self, response):
        _model = _AllOrdersResp(data=response)
        return _model.data
        
       


if __name__ == "__main__":

    data = [
  {
    "symbol": "LTCBTC",
    "orderId": 1,
    "orderListId": -1,
    "clientOrderId": "myOrder1",
    "price": "0.1",
    "origQty": "1.0",
    "executedQty": "0.0",
    "cummulativeQuoteQty": "0.0",
    "status": "NEW",
    "timeInForce": "GTC",
    "type": "LIMIT",
    "side": "BUY",
    "stopPrice": "0.0",
    "icebergQty": "0.0",
    "time": 1499827319559,
    "updateTime": 1499827319559,
    "isWorking": True,
    "origQuoteOrderQty": "0.000000"
  }
]

    model = Response()
    model(data)