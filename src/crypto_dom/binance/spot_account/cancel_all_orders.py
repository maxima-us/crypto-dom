import typing
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import  ORDER_SIDE, ORDER_STATUS, ORDER_TYPE, ORDER_TIF, RECV_WINDOW, SYMBOL


# ============================================================
# CANCEL ALL OPEN ORDERS (TRADE)
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#cancel-all-open-orders-on-a-symbol-trade

URL = "https://api.binance.com/api/v3/openOrders"
METHOD = "DELETE"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


# [
#   {
#     "symbol": "BTCUSDT",
#     "origClientOrderId": "E6APeyTJvkMvLMYMqu1KQ4",
#     "orderId": 11,
#     "orderListId": -1,
#     "clientOrderId": "pXLV6Hz6mprAcVYpVMTGgx",
#     "price": "0.089853",
#     "origQty": "0.178622",
#     "executedQty": "0.000000",
#     "cummulativeQuoteQty": "0.000000",
#     "status": "CANCELED",
#     "timeInForce": "GTC",
#     "type": "LIMIT",
#     "side": "BUY"
#   },
#   {
#     "symbol": "BTCUSDT",
#     "origClientOrderId": "A3EF2HCwxgZPFMrfwbgrhv",
#     "orderId": 13,
#     "orderListId": -1,
#     "clientOrderId": "pXLV6Hz6mprAcVYpVMTGgx",
#     "price": "0.090430",
#     "origQty": "0.178622",
#     "executedQty": "0.000000",
#     "cummulativeQuoteQty": "0.000000",
#     "status": "CANCELED",
#     "timeInForce": "GTC",
#     "type": "LIMIT",
#     "side": "BUY"
#   },
#   {
#     "orderListId": 1929,
#     "contingencyType": "OCO",
#     "listStatusType": "ALL_DONE",
#     "listOrderStatus": "ALL_DONE",
#     "listClientOrderId": "2inzWQdDvZLHbbAmAozX2N",
#     "transactionTime": 1585230948299,
#     "symbol": "BTCUSDT",
#     "orders": [
#       {
#         "symbol": "BTCUSDT",
#         "orderId": 20,
#         "clientOrderId": "CwOOIPHSmYywx6jZX77TdL"
#       },
#       {
#         "symbol": "BTCUSDT",
#         "orderId": 21,
#         "clientOrderId": "461cPg51vQjV3zIMOXNz39"
#       }
#     ],
#     "orderReports": [
#       {
#         "symbol": "BTCUSDT",
#         "origClientOrderId": "CwOOIPHSmYywx6jZX77TdL",
#         "orderId": 20,
#         "orderListId": 1929,
#         "clientOrderId": "pXLV6Hz6mprAcVYpVMTGgx",
#         "price": "0.668611",
#         "origQty": "0.690354",
#         "executedQty": "0.000000",
#         "cummulativeQuoteQty": "0.000000",
#         "status": "CANCELED",
#         "timeInForce": "GTC",
#         "type": "STOP_LOSS_LIMIT",
#         "side": "BUY",
#         "stopPrice": "0.378131",
#         "icebergQty": "0.017083"
#       },
#       {
#         "symbol": "BTCUSDT",
#         "origClientOrderId": "461cPg51vQjV3zIMOXNz39",
#         "orderId": 21,
#         "orderListId": 1929,
#         "clientOrderId": "pXLV6Hz6mprAcVYpVMTGgx",
#         "price": "0.008791",
#         "origQty": "0.690354",
#         "executedQty": "0.000000",
#         "cummulativeQuoteQty": "0.000000",
#         "status": "CANCELED",
#         "timeInForce": "GTC",
#         "type": "LIMIT_MAKER",
#         "side": "BUY",
#         "icebergQty": "0.639962"
#       }
#     ]
#   }
# ]


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint DELETE https://api.binance.com/api/v3/openOrders

    Model Fields:
    -------------
        symbol : str
        timestamp : float
        recvWindow : int
           Number of milliseconds after timestamp the request is valid for (optional)
           Default = 5000

    """

    symbol: SYMBOL

    timestamp: TIMESTAMP_MS
    recvWindow: typing.Optional[RECV_WINDOW]


# ------------------------------
# Response Model
# ------------------------------


class _StandardOrder(pydantic.BaseModel):

    symbol: SYMBOL
    origClientOrderId: str
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


class _OCOOrder(pydantic.BaseModel):


    class _Order(pydantic.BaseModel):
        symbol: SYMBOL
        orderId: pydantic.PositiveInt
        clientOrderId: str

    class _OrderReport(pydantic.BaseModel):
        symbol: SYMBOL
        origClientOrderId: str
        orderId: pydantic.PositiveInt
        orderListId: pydantic.PositiveInt
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


    orderListId: pydantic.PositiveInt
    contingencyType: Literal["OCO"]
    listStatusType: Literal["ALL_DONE"]
    listOrderStatus: Literal["ALL_DONE"]
    listClientOrderId: str
    transactionTime: TIMESTAMP_MS
    symbol: SYMBOL
    orders: typing.Tuple[_Order, ...]
    orderReports: typing.Tuple[_OrderReport, ...]


class _CancelAllOrdersResp(pydantic.BaseModel):
    
    data: typing.Tuple[typing.Union[_StandardOrder, _OCOOrder], ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint DELETE https://api.binance.com/api/v3/openOrders

    Type: tuple of pydantic.BaseModel

    Model Fields:
    -------------
    """

    def __call__(self, response):
        _model = _CancelAllOrdersResp(data=response)
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