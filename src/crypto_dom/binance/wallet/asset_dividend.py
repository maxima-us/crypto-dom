
import typing
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS, COUNT


# ============================================================
# DEPOSIT HISTORY (SUPPORTING NETWORK) 
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#asset-dividend-record-user_data

URL = "https://api.binance.com/sapi/v1/asset/assetDividend"
METHOD = "GET"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


# {
#     "rows":[
#         {
#             "amount":"10.00000000",
#             "asset":"BHFT",
#             "divTime":1563189166000,
#             "enInfo":"BHFT distribution",
#             "tranId":2968885920
#         },
#         {
#             "amount":"10.00000000",
#             "asset":"BHFT",
#             "divTime":1563189165000,
#             "enInfo":"BHFT distribution",
#             "tranId":2968885920
#         }
#     ],
#     "total":2
# }


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint https://api.binance.com/sapi/v1/asset/assetDividend

    Model Fields:
    -------------
        asset : str 
        limit : int
            (optional)
        startTime : float
            Timestamp in milliseconds (optional)
        endTime : float
            Timestamp in milliseconds (optional)
        timestamp : float
        recvWindow : int
           Number of milliseconds after timestamp the request is valid for (optional)
           Default = 5000
       
    """

    asset: str # TODO add asset type
  
    limit: typing.Optional[int]
    startTime: typing.Optional[TIMESTAMP_MS]
    endTime: typing.Optional[TIMESTAMP_MS]

    timestamp: TIMESTAMP_MS     #FIXME what is this ?
    recvWindow: typing.Optional[pydantic.conint(le=60000)] # TODO add to definitions


# ------------------------------
# Response Model
# ------------------------------


class _Dividend(pydantic.BaseModel):
    
    amount: Decimal
    asset: str # TODO replace with Asset
    divTime: TIMESTAMP_MS
    enInfo: str
    tranId: int


class _AssetDividendResp(pydantic.BaseModel):

    row: typing.Tuple[_Dividend, ...]
    total: COUNT


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint https://api.binance.com/sapi/v1/asset/assetDividend

    Type: pydantic.BaseModel or array of pydantic Models
    
    Model Fields:
    -------------
    """

    def __new__(_cls):
        return _AssetDividendResp
        




if __name__ == "__main__":

    data = {
    "rows":[
        {
            "amount":"10.00000000",
            "asset":"BHFT",
            "divTime":1563189166000,
            "enInfo":"BHFT distribution",
            "tranId":2968885920
        },
        {
            "amount":"10.00000000",
            "asset":"BHFT",
            "divTime":1563189165000,
            "enInfo":"BHFT distribution",
            "tranId":2968885920
        }
    ],
    "total":2
}

    expect = Response()
    valid = expect(**data)
    print("Validated model", valid, "\n")