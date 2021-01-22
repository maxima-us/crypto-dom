import typing

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import OCO_ORDER_STATUS, OCO_STATUS, RECV_WINDOW, SYMBOL


# ============================================================
# QUERY ALL OCO (USER DATA)
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#query-all-oco-user_data

URL = "https://api.binance.com/api/v3/allOrderList"
METHOD = "GET"
WEIGHT = 10


# ------------------------------
# Sample Response (doc)
# ------------------------------


# [
#   {
#     "orderListId": 29,
#     "contingencyType": "OCO",
#     "listStatusType": "EXEC_STARTED",
#     "listOrderStatus": "EXECUTING",
#     "listClientOrderId": "amEEAXryFzFwYF1FeRpUoZ",
#     "transactionTime": 1565245913483,
#     "symbol": "LTCBTC",
#     "orders": [
#       {
#         "symbol": "LTCBTC",
#         "orderId": 4,
#         "clientOrderId": "oD7aesZqjEGlZrbtRpy5zB"
#       },
#       {
#         "symbol": "LTCBTC",
#         "orderId": 5,
#         "clientOrderId": "Jr1h6xirOxgeJOUuYQS7V3"
#       }
#     ]
#   },
#   {
#     "orderListId": 28,
#     "contingencyType": "OCO",
#     "listStatusType": "EXEC_STARTED",
#     "listOrderStatus": "EXECUTING",
#     "listClientOrderId": "hG7hFNxJV6cZy3Ze4AUT4d",
#     "transactionTime": 1565245913407,
#     "symbol": "LTCBTC",
#     "orders": [
#       {
#         "symbol": "LTCBTC",
#         "orderId": 2,
#         "clientOrderId": "j6lFOfbmFMRjTYA7rRJ0LP"
#       },
#       {
#         "symbol": "LTCBTC",
#         "orderId": 3,
#         "clientOrderId": "z0KCjOdditiLS5ekAFtK81"
#       }
#     ]
#   }
# ]


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint GET https://api.binance.com/api/v3/allOrderList
    
    Model Fields:
    -------------
        fromId : int
            (optional)
        startTime : float
            Timestamp in milliseconds (optional)
        endTime : float
            Timestamp in milliseconds (optional)
        limit : int
            Default = 500; Max = 1000 (optional)
        timestamp : float
        recvWindow : int
           Number of milliseconds after timestamp the request is valid for (optional)
           Default = 5000
    """

    fromId: typing.Optional[int]
    startTime: typing.Optional[TIMESTAMP_MS]
    endTime: typing.Optional[TIMESTAMP_MS]
    limit: typing.Optional[pydantic.conint(ge=0, le=1000)]

    timestamp: TIMESTAMP_MS
    recvWindow: typing.Optional[RECV_WINDOW]
    
    
    @pydantic.validator("endTime")
    def _check_mandatory_args(cls, v, values):

        if v or values.get("startTime"):
            if values.get("fromId"):
                raise ValueError("If fromId is supplied, neither startTime or endTime can be provided")

        return v


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


class _QueryAllOCOResp(pydantic.BaseModel):

    # placeholder
    data: typing.Tuple[_OCOResp, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint GET https://api.binance.com/api/v3/allOrderList

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
        model = _QueryAllOCOResp(data=response)
        return model.data
        
   
    



if __name__ == "__main__":
  
    data = [
  {
    "orderListId": 29,
    "contingencyType": "OCO",
    "listStatusType": "EXEC_STARTED",
    "listOrderStatus": "EXECUTING",
    "listClientOrderId": "amEEAXryFzFwYF1FeRpUoZ",
    "transactionTime": 1565245913483,
    "symbol": "LTCBTC",
    "orders": [
      {
        "symbol": "LTCBTC",
        "orderId": 4,
        "clientOrderId": "oD7aesZqjEGlZrbtRpy5zB"
      },
      {
        "symbol": "LTCBTC",
        "orderId": 5,
        "clientOrderId": "Jr1h6xirOxgeJOUuYQS7V3"
      }
    ]
  },
  {
    "orderListId": 28,
    "contingencyType": "OCO",
    "listStatusType": "EXEC_STARTED",
    "listOrderStatus": "EXECUTING",
    "listClientOrderId": "hG7hFNxJV6cZy3Ze4AUT4d",
    "transactionTime": 1565245913407,
    "symbol": "LTCBTC",
    "orders": [
      {
        "symbol": "LTCBTC",
        "orderId": 2,
        "clientOrderId": "j6lFOfbmFMRjTYA7rRJ0LP"
      },
      {
        "symbol": "LTCBTC",
        "orderId": 3,
        "clientOrderId": "z0KCjOdditiLS5ekAFtK81"
      }
    ]
  }
]

    model = Response()
    model(data)