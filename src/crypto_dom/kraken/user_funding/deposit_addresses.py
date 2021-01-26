import typing
from decimal import Decimal
from crypto_dom.definitions import TIMESTAMP_S

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.kraken.definitions import ASSETCLASS, ASSET


# ============================================================
# DEPOSIT ADDRESSES 
# ============================================================


# doc: https://www.kraken.com/features/api#deposit-addresses

URL = "https://api.kraken.com/0/private/DepositAddresses"
METHOD = "POST"


# ------------------------------
# Sample Response
# ------------------------------



# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint POST https://api.kraken.com/0/private/DepositAddresses

    Model Fields:
    -------------
        aclass : str
            Default = currency (optional)
        asset : str enum
            Asset being deposited
        method : str
            Name of the deposit method
        new : bool
            Whether or not to generate a new address (optional)
            Default = False
        nonce : int
            Always increasing unsigned 64 bit integer 
    """

    aclass: typing.Optional[ASSETCLASS]
    asset: ASSET
    method: str     # TODO this should be an enum
    new: typing.Optional[bool]
    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
# ------------------------------


class _DepositAddressesResponse(pydantic.BaseModel):
    address: str
    expiretm: TIMESTAMP_S
    new: bool


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint POST https://api.kraken.com/0/private/DepositAddresses

    Type: pydantic Model

    Model Fields:
    -------------
        address : str
            Deposit Address
        expiretm : float
            Expiration timestamp in seconds (0 if not expiring)
        new : boool
            Wether or not address has ever been used
    """

    def __call__(self, response: dict):
        return _DepositAddressesResponse(**response)
        
    