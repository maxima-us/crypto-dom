import typing
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import OCO_ORDER_STATUS, OCO_STATUS, ORDER_RESP_TYPE, ORDER_SIDE, ORDER_STATUS, ORDER_TYPE, ORDER_TIF, RECV_WINDOW, SYMBOL, ASSET


# ============================================================
# NEW OCO (TRADE)
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#new-oco-trade

URL = "https://api.binance.com/api/v3/order/oco"
METHOD = "POST"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


# {
#   "orderListId": 0,
#   "contingencyType": "OCO",
#   "listStatusType": "EXEC_STARTED",
#   "listOrderStatus": "EXECUTING",
#   "listClientOrderId": "JYVpp3F0f5CAG15DhtrqLp",
#   "transactionTime": 1563417480525,
#   "symbol": "LTCBTC",
#   "orders": [
#     {
#       "symbol": "LTCBTC",
#       "orderId": 2,
#       "clientOrderId": "Kk7sqHb9J6mJWTMDVW7Vos"
#     },
#     {
#       "symbol": "LTCBTC",
#       "orderId": 3,
#       "clientOrderId": "xTXKaGYd4bluPVp78IVRvl"
#     }
#   ],
#   "orderReports": [
#     {
#       "symbol": "LTCBTC",
#       "orderId": 2,
#       "orderListId": 0,
#       "clientOrderId": "Kk7sqHb9J6mJWTMDVW7Vos",
#       "transactTime": 1563417480525,
#       "price": "0.000000",
#       "origQty": "0.624363",
#       "executedQty": "0.000000",
#       "cummulativeQuoteQty": "0.000000",
#       "status": "NEW",
#       "timeInForce": "GTC",
#       "type": "STOP_LOSS",
#       "side": "BUY",
#       "stopPrice": "0.960664"
#     },
#     {
#       "symbol": "LTCBTC",
#       "orderId": 3,
#       "orderListId": 0,
#       "clientOrderId": "xTXKaGYd4bluPVp78IVRvl",
#       "transactTime": 1563417480525,
#       "price": "0.036435",
#       "origQty": "0.624363",
#       "executedQty": "0.000000",
#       "cummulativeQuoteQty": "0.000000",
#       "status": "NEW",
#       "timeInForce": "GTC",
#       "type": "LIMIT_MAKER",
#       "side": "BUY"
#     }
#   ]
# }


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint POST https://api.binance.com/api/v3/order/oco

    Model Fields:
    -------------

        symbol : str
        listClientOrderId: str
            A unique Id for the entire orderList (optional)
        side : str enum
            [BUY, SELL]
        quantity : Decimal
        limitClientOrderId: str
            A unique Id for the limit order (optional)
        price : Decimal
        limitIcebergQty: Decimal
            (optional)
        stopClientOrderId: str
            A unique Id for the stop loss/stop loss limit leg (optional)
        stopPrice: Decimal
        stopLimitPrice: Decimal
            If provided, stopLimitTimeInForce is required. (optional)
        stopIcebergQty: Decimal
            (optional)
        stopLimitTimeInForce: str enum
            [GTC, FOK, IOC] (optional)
        newOrderRespType : str enum
            [ACK, RESULT, FULL] (optional)

        timestamp : float
        recvWindow : int
           Number of milliseconds after timestamp the request is valid for (optional)
           Default = 5000

    """

    symbol: SYMBOL
    listClientOrderId: typing.Optional[str]
    side: ORDER_SIDE
    quantity: Decimal
    limitClientOrderId: typing.Optional[str]
    price: Decimal
    limitIcebergQty: typing.Optional[Decimal]
    stopClientOrderId: typing.Optional[str]
    stopPrice: Decimal
    stopLimitPrice: typing.Optional[Decimal]
    stopIcebergQty: typing.Optional[Decimal]
    stopLimitTimeInForce: typing.Optional[ORDER_TIF]
    newOrderRespType: typing.Optional[ORDER_RESP_TYPE]

    timestamp: TIMESTAMP_MS
    recvWindow: typing.Optional[RECV_WINDOW]


# ------------------------------
# Response Model
# ------------------------------


class _Order(pydantic.BaseModel):
    symbol: SYMBOL
    orderId: pydantic.PositiveInt
    clientOrderId: str


class _OrderReport(pydantic.BaseModel):
    symbol: SYMBOL
    orderId: pydantic.PositiveInt
    orderListId: int 
    clientOrderId: str
    transactTime: TIMESTAMP_MS
    price: Decimal
    origQty: Decimal
    executedQty: Decimal
    cummulativeQuoteQty: Decimal
    status: ORDER_STATUS
    timeInForce: ORDER_TIF
    type: ORDER_TYPE
    side: ORDER_SIDE
    stopPrice: typing.Optional[Decimal]


class _NewOCOResp(pydantic.BaseModel):

    orderListId: int
    contingencyType: Literal["OCO"]     # TODO add rest of enums
    listStatusType: OCO_STATUS
    listOrderStatus: OCO_ORDER_STATUS
    listClientOrderId: str
    transactionTime: TIMESTAMP_MS
    symbol: SYMBOL
    orders: typing.Tuple[_Order, ...]
    orderReports: typing.Tuple[_OrderReport, ...]



#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint POST https://api.binance.com/api/v3/order/oco

    Type: pydantic Model 

    Model Fields:
    -------------
        orderListId: int
        contigencyType: str enum
        listStatusType: str enum
        listOrderStatus: str enum
        listClientOrderId: str enum
        transactionTime: float
            Timestamp in milliseconds
        symbol: str
        orders: Tuple[pydantic.BaseModel]
        orderReports: Tuple[pydantic.BaseModel]
    """

    def __new__(_cls):
        return _NewOCOResp
        
   
    



if __name__ == "__main__":
  
    data = {
          "orderListId": 0,
  "contingencyType": "OCO",
  "listStatusType": "EXEC_STARTED",
  "listOrderStatus": "EXECUTING",
  "listClientOrderId": "JYVpp3F0f5CAG15DhtrqLp",
  "transactionTime": 1563417480525,
  "symbol": "LTCBTC",
  "orders": [
    {
      "symbol": "LTCBTC",
      "orderId": 2,
      "clientOrderId": "Kk7sqHb9J6mJWTMDVW7Vos"
    },
    {
      "symbol": "LTCBTC",
      "orderId": 3,
      "clientOrderId": "xTXKaGYd4bluPVp78IVRvl"
    }
  ],
  "orderReports": [
    {
      "symbol": "LTCBTC",
      "orderId": 2,
      "orderListId": 0,
      "clientOrderId": "Kk7sqHb9J6mJWTMDVW7Vos",
      "transactTime": 1563417480525,
      "price": "0.000000",
      "origQty": "0.624363",
      "executedQty": "0.000000",
      "cummulativeQuoteQty": "0.000000",
      "status": "NEW",
      "timeInForce": "GTC",
      "type": "STOP_LOSS",
      "side": "BUY",
      "stopPrice": "0.960664"
    },
    {
      "symbol": "LTCBTC",
      "orderId": 3,
      "orderListId": 0,
      "clientOrderId": "xTXKaGYd4bluPVp78IVRvl",
      "transactTime": 1563417480525,
      "price": "0.036435",
      "origQty": "0.624363",
      "executedQty": "0.000000",
      "cummulativeQuoteQty": "0.000000",
      "status": "NEW",
      "timeInForce": "GTC",
      "type": "LIMIT_MAKER",
      "side": "BUY"
    }
  ]
}

    model = Response()
    model(**data)