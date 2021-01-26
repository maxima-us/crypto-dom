import typing

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.kraken.definitions import ASSETCLASS, ASSET


# ============================================================
# CANCEL WITHDRAWAL 
# ============================================================


# doc: https://www.kraken.com/features/api#withdraw-cancel

URL = "https://api.kraken.com/0/private/WithdrawCancel"
METHOD = "POST"


# ------------------------------
# Sample Response
# ------------------------------



# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint POST https://api.kraken.com/0/private/WithdrawCancel

    Model Fields:
    -------------
        aclass : str
            Default = currency (optional)
        asset : str enum
            Asset being withdrawn
        refid : str
            Withdrawal reference id 
        nonce : int
            Always increasing unsigned 64 bit integer 
    """

    aclass: typing.Optional[ASSETCLASS]
    asset: ASSET
    refid: str

    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
# ------------------------------


class _WithdrawCancelResp(pydantic.BaseModel):
    
    #placeholder
    data: bool 


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint POST https://api.kraken.com/0/private/WithdrawCancel

    Type: bool (True on success)
    """

    def __call__(self, response: dict):
        _valid = _WithdrawCancelResp(data=response)
        return _valid.data
    