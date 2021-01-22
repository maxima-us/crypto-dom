import typing
from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import  ORDER_SIDE, ORDER_STATUS, ORDER_TYPE, ORDER_TIF, RECV_WINDOW, SYMBOL


# ============================================================
# QUERY ORDER (USER DATA)
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#query-order-user_data

URL = "https://api.binance.com/api/v3/order"
METHOD = "GET"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


# {
#   "symbol": "LTCBTC",
#   "orderId": 1,
#   "orderListId": -1, //Unless OCO, value will be -1
#   "clientOrderId": "myOrder1",
#   "price": "0.1",
#   "origQty": "1.0",
#   "executedQty": "0.0",
#   "cummulativeQuoteQty": "0.0",
#   "status": "NEW",
#   "timeInForce": "GTC",
#   "type": "LIMIT",
#   "side": "BUY",
#   "stopPrice": "0.0",
#   "icebergQty": "0.0",
#   "time": 1499827319559,
#   "updateTime": 1499827319559,
#   "isWorking": true,
#   "origQuoteOrderQty": "0.000000"
# }


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint GET https://api.binance.com/api/v3/order

    Model Fields:
    -------------
        symbol : str
        orderId : int
            (optional)
        origClientOrderId : str
            (optional)
        timestamp : float
        recvWindow : int
           Number of milliseconds after timestamp the request is valid for (optional)
           Default = 5000

    """

    symbol: SYMBOL
    orderId: typing.Optional[int]
    origClientOrderId: typing.Optional[str]

    timestamp: TIMESTAMP_MS
    recvWindow: typing.Optional[RECV_WINDOW]


    @pydantic.validator("origClientOrderId")
    def _check_mandatory_args(cls, v, values):

        if v is None:
            if values.get("orderId") is None:
                raise ValueError("Either orderId or origClientOrderId must be sent")

        return v


# ------------------------------
# Response Model
# ------------------------------


class _QueryOrderResp(pydantic.BaseModel):

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


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint GET https://api.binance.com/api/v3/order

    Type: pydantic.BaseModel

    Model Fields:
    -------------
        symbol: str
        origClientOrderId: str
        orderId: int
        orderListId: int
            Unless part of an OCO, the value will always be -1
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

    def __new__(_cls):
        return _QueryOrderResp 
       



if __name__ == "__main__":

    data = {
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

    model = Response()
    model(**data)