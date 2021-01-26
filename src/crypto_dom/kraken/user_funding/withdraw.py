import typing
from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.kraken.definitions import ASSETCLASS, ASSET


# ============================================================
# WITHDRAW FUNDS 
# ============================================================


# doc: https://www.kraken.com/features/api#withdraw-funds 

URL = "https://api.kraken.com/0/private/Withdraw"
METHOD = "POST"


# ------------------------------
# Sample Response
# ------------------------------



# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint POST https://api.kraken.com/0/private/Withdraw

    Model Fields:
    -------------
        aclass : str
            Default = currency (optional)
        asset : str enum
            Asset being withdrawn
        key : str
            Withdrawal key name, as set up on account 
        amount : Decimal
            Amount to withdraw, including fees
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


class _WithdrawResponse(pydantic.BaseModel):
    refid: str
    

#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint POST https://api.kraken.com/0/private/Withdraw

    Type: pydantic Model

    Model Fields:
    -------------
        refid : str
            Reference id 
    """

    def __call__(self, response: dict):
        return _WithdrawResponse(**response)
        
    