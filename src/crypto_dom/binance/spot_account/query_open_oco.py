import typing

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import OCO_ORDER_STATUS, OCO_STATUS, RECV_WINDOW, SYMBOL


# ============================================================
# QUERY OPEN OCO (USER DATA)
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#query-open-oco-user_data

URL = "https://api.binance.com/api/v3/openOrderList"
METHOD = "GET"
WEIGHT = 2


# ------------------------------
# Sample Response (doc)
# ------------------------------


# [
#   {
#     "orderListId": 31,
#     "contingencyType": "OCO",
#     "listStatusType": "EXEC_STARTED",
#     "listOrderStatus": "EXECUTING",
#     "listClientOrderId": "wuB13fmulKj3YjdqWEcsnp",
#     "transactionTime": 1565246080644,
#     "symbol": "1565246079109",
#     "orders": [
#       {
#         "symbol": "LTCBTC",
#         "orderId": 4,
#         "clientOrderId": "r3EH2N76dHfLoSZWIUw1bT"
#       },
#       {
#         "symbol": "LTCBTC",
#         "orderId": 5,
#         "clientOrderId": "Cv1SnyPD3qhqpbjpYEHbd2"
#       }
#     ]
#   }
# ]


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint GET https://api.binance.com/api/v3/openOrderList
    
    Model Fields:
    -------------
        timestamp : float
        recvWindow : int
           Number of milliseconds after timestamp the request is valid for (optional)
           Default = 5000
    """

    timestamp: TIMESTAMP_MS
    recvWindow: typing.Optional[RECV_WINDOW]
    
    
# ------------------------------
# Response Model
# ------------------------------


class _Order(pydantic.BaseModel):
    symbol: SYMBOL
    orderId: pydantic.PositiveInt
    clientOrderId: str


class _OCOResp(pydantic.BaseModel):
    orderListId: int
    contingencyType: Literal["OCO"]     # TODO add rest of enums
    listStatusType: OCO_STATUS
    listOrderStatus: OCO_ORDER_STATUS
    listClientOrderId: str
    transactionTime: TIMESTAMP_MS
    symbol: SYMBOL
    orders: typing.Tuple[_Order, ...]


class _QueryOpenOCOResp(pydantic.BaseModel):

    # placeholder
    data: typing.Tuple[_OCOResp, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint GET https://api.binance.com/api/v3/openOrderList

    Type: array of pydantic Models

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
    """

    def __call__(_cls, response):
        model = _QueryOpenOCOResp(data=response)
        return model.data
        
   
    



if __name__ == "__main__":
  
    data = [
          {
    "orderListId": 31,
    "contingencyType": "OCO",
    "listStatusType": "EXEC_STARTED",
    "listOrderStatus": "EXECUTING",
    "listClientOrderId": "wuB13fmulKj3YjdqWEcsnp",
    "transactionTime": 1565246080644,
    "symbol": "BTCUSDT",        #! in doc value given is : "1565246079109" (very probably false)
    "orders": [
      {
        "symbol": "LTCBTC",
        "orderId": 4,
        "clientOrderId": "r3EH2N76dHfLoSZWIUw1bT"
      },
      {
        "symbol": "LTCBTC",
        "orderId": 5,
        "clientOrderId": "Cv1SnyPD3qhqpbjpYEHbd2"
      }
    ]
  }
]

    model = Response()
    model(data)