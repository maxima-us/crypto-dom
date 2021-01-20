import typing

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import RECV_WINDOW, ASSET


# ============================================================
# USER UNIVERSAL TRANSFER 
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#user-universal-transfer

URL = "https://api.binance.com/sapi/v1/asset/transfer"
METHOD = "GET"
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
    """Request model for endpoint https://api.binance.com/sapi/v1/asset/transfer

    Model Fields:
    -------------
        type : enum
            Enum Types: 
            MAIN_C2C Spot account transfer to C2C account
            MAIN_UMFUTURE Spot account transfer to USDⓈ-M Futures account
            MAIN_CMFUTURE Spot account transfer to COIN-M Futures account
            MAIN_MARGIN Spot account transfer to Margin（cross）account
            MAIN_MINING Spot account transfer to Mining account
            C2C_MAIN C2C account transfer to Spot account
            C2C_UMFUTURE C2C account transfer to USDⓈ-M Futures account
            C2C_MINING C2C account transfer to Mining account
            UMFUTURE_MAIN USDⓈ-M Futures account transfer to Spot account
            UMFUTURE_C2C USDⓈ-M Futures account transfer to C2C account
            UMFUTURE_MARGIN USDⓈ-M Futures account transfer to Margin（cross）account
            CMFUTURE_MAIN COIN-M Futures account transfer to Spot account
            MARGIN_MAIN Margin（cross）account transfer to Spot account
            MARGIN_UMFUTURE Margin（cross）account transfer to USDⓈ-M Futures
            MINING_MAIN Mining account transfer to Spot account
            MINING_UMFUTURE Mining account transfer to USDⓈ-M Futures account
            MINING_C2C Mining account transfer to C2C account
        asset : str
        timestamp : float
        recvWindow : int
           Number of milliseconds after timestamp the request is valid for (optional)
           Default = 5000
       
    """

    type: Literal[
        "MAIN_C2C",
        "MAIN_UMFUTURE",
        "MAIN_CMFUTURE",
        "MAIN_MARGIN",
        "MAIN_MINING",
        "C2C_MAIN",
        "C2C_UMFUTURE",
        "C2C_MINING",
        "UMFUTURE_MAIN",
        "UMFUTURE_C2C",
        "UMFUTURE_MARGIN",
        "CMFUTURE_MAIN",
        "MARGIN_MAIN",
        "MARGIN_UMFUTURE",
        "MINING_MAIN",
        "MINING_UMFUTURE",
        "MINING_C2C"
    ] 
    asset: ASSET 
    timestamp: TIMESTAMP_MS
    recvWindow: typing.Optional[RECV_WINDOW]


# ------------------------------
# Response Model
# ------------------------------


class _AssetTransferResp(pydantic.BaseModel):

    tranId: int 


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint https://api.binance.com/sapi/v1/asset/transfer

    Type: pydantic.BaseModel or array of pydantic Models
    
    Model Fields:
    -------------
    """

    def __new__(_cls):
        return _AssetTransferResp
        