import typing
from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.kraken.definitions import ASSETCLASS, ASSET


# ============================================================
# WITHDRAWAL INFO
# ============================================================


# doc: https://www.kraken.com/features/api#get-withdrawal-info

URL = "https://api.kraken.com/0/private/WithdrawInfo"
METHOD = "POST"


# ------------------------------
# Sample Response
# ------------------------------



# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint POST https://api.kraken.com/0/private/WithdrawInfo

    Model Fields:
    -------------
        aclass : str
            Default = currency (optional)
        asset : str enum
            Asset being withdrawn
        key : str
            Withdrawal key name, as set up on account 
        amount : Decimal
            Amount to withdraw
        nonce : int
            Always increasing unsigned 64 bit integer 
    """

    aclass: typing.Optional[ASSETCLASS]
    asset: ASSET
    key: str
    amount: Decimal

    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
# ------------------------------


class _WithdrawInfoResponse(pydantic.BaseModel):
    method: str # TODO should be Literal
    limit: Decimal
    fee: Decimal


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint POST https://api.kraken.com/0/private/WithdrawInfo

    Type: pydantic Model

    Model Fields:
    -------------
        method : str enum
            Name of the deposit method used
        limit : Decimal
            Maximum net amount that can be withdrawn right now 
        fee : Decimal
            Fees paid
    """

    def __call__(self, response: dict):
        return _WithdrawInfoResponse(**response)
        
    