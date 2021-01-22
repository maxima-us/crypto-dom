import typing
from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import  ORDER_SIDE, ORDER_STATUS, ORDER_TYPE, ORDER_TIF, RECV_WINDOW, SYMBOL


# ============================================================
# CURRENT OPEN ORDERS (USER DATA)
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#current-open-orders-user_data

URL = "https://api.binance.com/api/v3/openOrders"
METHOD = "GET"
WEIGHT = 1  # 40 if symbol parameter is ommited


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
    """Request model for endpoint GET https://api.binance.com/api/v3/openOrders

    Model Fields:
    -------------
        symbol : str
            If symbol is ommited, request weight = 40 (optional)
        timestamp : float
            Timestamp in millisecond
        recvWindow : int
           Number of milliseconds after timestamp the request is valid for (optional)
           Default = 5000

    """

    symbol: typing.Optional[SYMBOL]

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


class _QueryOrdersResp(pydantic.BaseModel):
    
    data: typing.Tuple[_Order, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint GET https://api.binance.com/api/v3/openOrders

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
        _model = _QueryOrdersResp(data=response)
        return _model.data
        
       


if __name__ == "__main__":

    data = [
  {
    "symbol": "BTCUSDT",
    "origClientOrderId": "E6APeyTJvkMvLMYMqu1KQ4",
    "orderId": 11,
    "orderListId": -1,
    "clientOrderId": "pXLV6Hz6mprAcVYpVMTGgx",
    "price": "0.089853",
    "origQty": "0.178622",
    "executedQty": "0.000000",
    "cummulativeQuoteQty": "0.000000",
    "status": "CANCELED",
    "timeInForce": "GTC",
    "type": "LIMIT",
    "side": "BUY"
  },
  {
    "symbol": "BTCUSDT",
    "origClientOrderId": "A3EF2HCwxgZPFMrfwbgrhv",
    "orderId": 13,
    "orderListId": -1,
    "clientOrderId": "pXLV6Hz6mprAcVYpVMTGgx",
    "price": "0.090430",
    "origQty": "0.178622",
    "executedQty": "0.000000",
    "cummulativeQuoteQty": "0.000000",
    "status": "CANCELED",
    "timeInForce": "GTC",
    "type": "LIMIT",
    "side": "BUY"
  },
  {
    "orderListId": 1929,
    "contingencyType": "OCO",
    "listStatusType": "ALL_DONE",
    "listOrderStatus": "ALL_DONE",
    "listClientOrderId": "2inzWQdDvZLHbbAmAozX2N",
    "transactionTime": 1585230948299,
    "symbol": "BTCUSDT",
    "orders": [
      {
        "symbol": "BTCUSDT",
        "orderId": 20,
        "clientOrderId": "CwOOIPHSmYywx6jZX77TdL"
      },
      {
        "symbol": "BTCUSDT",
        "orderId": 21,
        "clientOrderId": "461cPg51vQjV3zIMOXNz39"
      }
    ],
    "orderReports": [
      {
        "symbol": "BTCUSDT",
        "origClientOrderId": "CwOOIPHSmYywx6jZX77TdL",
        "orderId": 20,
        "orderListId": 1929,
        "clientOrderId": "pXLV6Hz6mprAcVYpVMTGgx",
        "price": "0.668611",
        "origQty": "0.690354",
        "executedQty": "0.000000",
        "cummulativeQuoteQty": "0.000000",
        "status": "CANCELED",
        "timeInForce": "GTC",
        "type": "STOP_LOSS_LIMIT",
        "side": "BUY",
        "stopPrice": "0.378131",
        "icebergQty": "0.017083"
      },
      {
        "symbol": "BTCUSDT",
        "origClientOrderId": "461cPg51vQjV3zIMOXNz39",
        "orderId": 21,
        "orderListId": 1929,
        "clientOrderId": "pXLV6Hz6mprAcVYpVMTGgx",
        "price": "0.008791",
        "origQty": "0.690354",
        "executedQty": "0.000000",
        "cummulativeQuoteQty": "0.000000",
        "status": "CANCELED",
        "timeInForce": "GTC",
        "type": "LIMIT_MAKER",
        "side": "BUY",
        "icebergQty": "0.639962"
      }
    ]
  }
]

    model = Response()
    model(data)