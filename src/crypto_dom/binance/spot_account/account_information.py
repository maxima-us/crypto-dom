import typing
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import RECV_WINDOW, ASSET, SYMBOL_PERMISSIONS


# ============================================================
# ACCOUNT INFORMATION (USER DATA)
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#account-information-user_data

URL = "https://api.binance.com/api/v3/account"
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
    """Request model for endpoint GET https://api.binance.com/api/v3/account
    
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


class _Balance(pydantic.BaseModel):
    asset: str # ASSET missing DEXE
    free: Decimal
    locked: Decimal


class _AccountInformationResp(pydantic.BaseModel):
    makerCommission: pydantic.conint(ge=0)    
    takerCommission: pydantic.conint(ge=0)    
    buyerCommission: pydantic.conint(ge=0)    
    sellerCommission: pydantic.conint(ge=0)    
    canTrade: bool
    canWithdraw: bool
    canDeposit: bool
    updateTime: TIMESTAMP_MS
    accountType: Literal["SPOT", "MARGIN"]
    balances: typing.Tuple[_Balance, ...]
    permissions: typing.List[SYMBOL_PERMISSIONS]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint GET https://api.binance.com/api/v3/account

    Type: array of pydantic Models

    Model Fields:
    -------------
        makerCommission: int
        takerCommission: int
        buyerCommission: int
        sellerCommission: int
        canTrade: bool
        canWithdraw: bool
        canDeposit: bool
        updateTime: bool
        accountType: str enum
            [SPOT]
        balances: List[pydantic.BaseModel]

    """

    def __new__(_cls):
        return _AccountInformationResp
        
   
    



if __name__ == "__main__":
  
    data = {
  "makerCommission": 15,
  "takerCommission": 15,
  "buyerCommission": 0,
  "sellerCommission": 0,
  "canTrade": True,
  "canWithdraw": True,
  "canDeposit": True,
  "updateTime": 123456789,
  "accountType": "SPOT",
  "balances": [
    {
      "asset": "BTC",
      "free": "4723846.89208129",
      "locked": "0.00000000"
    },
    {
      "asset": "LTC",
      "free": "4763368.68006011",
      "locked": "0.00000000"
    }
  ],
  "permissions": [
    "SPOT"
  ]
}

    model = Response()
    model(**data)