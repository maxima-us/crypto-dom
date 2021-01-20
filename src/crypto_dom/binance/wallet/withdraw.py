
import typing
from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import RECV_WINDOW, ASSET


# ============================================================
# WITHDRAW 
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#withdraw-sapi

URL = "https://api.binance.com/sapi/v1/capital/withdraw/apply"
METHOD = "POST"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


# {
#     "tranId":13526853623
# }


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint https://api.binance.com/sapi/v1/capital/withdraw/apply

    Model Fields:
    -------------
        coin : str
        address : str
        amount : Decimal
        withdrawOrderId : str
            Client ID for withdraw (optional)
        network : str
            If not sent, return default network of the coin (optional)
            You can get network and isDefault in networkList in the response of "GET /sapi/v1/capital/config/getall" (HMAC SHA256).
        addressTag : str
            Secondary address identifier for certain coins (optional)
        transactionFeeFlag: bool
            When making internal transfer, true for returning the fee to the destination account; 
            false for returning the fee back to the departure account. Default false.
            (optional)
        name : str
            Description of the address. Space in name should be encoded into %20.
            (optional)
        timestamp : float
        recvWindow : int
           Number of milliseconds after timestamp the request is valid for (optional)
           Default = 5000
       
    """

    coin: ASSET
    address: str
    amount: Decimal
    withdrawOrderId: typing.Optional[str]
    network: typing.Optional[str]
    addressTag: typing.Optional[str]
    transactionFeeFlag: typing.Optional[bool]
    name: typing.Optional[str]

    timestamp: TIMESTAMP_MS
    recvWindow: typing.Optional[RECV_WINDOW]

# ------------------------------
# Response Model
# ------------------------------


class _WithdrawResp(pydantic.BaseModel):

    id: str 


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint https://api.binance.com/sapi/v1/capital/withdraw/apply

    Type: pydantic.BaseModel or array of pydantic Models
    
    Model Fields:
    -------------
    """

    def __new__(_cls):
        return _WithdrawResp
        