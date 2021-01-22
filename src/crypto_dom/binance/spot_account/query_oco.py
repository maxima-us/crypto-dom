import typing

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import OCO_ORDER_STATUS, OCO_STATUS, RECV_WINDOW, SYMBOL


# ============================================================
# QUERY OCO (USER DATA)
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#cancel-oco-trade

URL = "https://api.binance.com/api/v3/orderList"
METHOD = "GET"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


# {
#   "orderListId": 27,
#   "contingencyType": "OCO",
#   "listStatusType": "EXEC_STARTED",
#   "listOrderStatus": "EXECUTING",
#   "listClientOrderId": "h2USkA5YQpaXHPIrkd96xE",
#   "transactionTime": 1565245656253,
#   "symbol": "LTCBTC",
#   "orders": [
#     {
#       "symbol": "LTCBTC",
#       "orderId": 4,
#       "clientOrderId": "qD1gy3kc3Gx0rihm9Y3xwS"
#     },
#     {
#       "symbol": "LTCBTC",
#       "orderId": 5,
#       "clientOrderId": "ARzZ9I00CPM8i3NhmU9Ega"
#     }
#   ]
# }


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint GET https://api.binance.com/api/v3/orderList
    
    Model Fields:
    -------------
        orderListId: int
            (optional)
        origClientOrderId: str
            (optional)
        timestamp : float
        recvWindow : int
           Number of milliseconds after timestamp the request is valid for (optional)
           Default = 5000
    """

    orderListId: typing.Optional[int]
    origClientOrderId: typing.Optional[str]

    timestamp: TIMESTAMP_MS
    recvWindow: typing.Optional[RECV_WINDOW]
    
    
    @pydantic.validator("origClientOrderId")
    def _check_mandatory_args(cls, v, values):

        if v is None:
            if values.get("orderListId") is None:
                raise ValueError("Either orderListId or origClientOrderId must be provided")

        return v


# ------------------------------
# Response Model
# ------------------------------


class _Order(pydantic.BaseModel):
    symbol: SYMBOL
    orderId: pydantic.PositiveInt
    clientOrderId: str


class _QueryOCOResp(pydantic.BaseModel):
    orderListId: int
    contingencyType: Literal["OCO"]     # TODO add rest of enums
    listStatusType: OCO_STATUS
    listOrderStatus: OCO_ORDER_STATUS
    listClientOrderId: str
    transactionTime: TIMESTAMP_MS
    symbol: SYMBOL
    orders: typing.Tuple[_Order, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint GET https://api.binance.com/api/v3/orderList

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
    """

    def __new__(_cls):
        return _QueryOCOResp
        
   
    



if __name__ == "__main__":
  
    data = {
  "orderListId": 27,
  "contingencyType": "OCO",
  "listStatusType": "EXEC_STARTED",
  "listOrderStatus": "EXECUTING",
  "listClientOrderId": "h2USkA5YQpaXHPIrkd96xE",
  "transactionTime": 1565245656253,
  "symbol": "LTCBTC",
  "orders": [
    {
      "symbol": "LTCBTC",
      "orderId": 4,
      "clientOrderId": "qD1gy3kc3Gx0rihm9Y3xwS"
    },
    {
      "symbol": "LTCBTC",
      "orderId": 5,
      "clientOrderId": "ARzZ9I00CPM8i3NhmU9Ega"
    }
  ]
}

    model = Response()
    model(**data)