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


# [
#   {
#       'address': '0x28c80ba9fb362b4117128f7e0dd3400f2f131514', 
#       'expiretm': '0'
#   }
# ]


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


class _DepositAddress(pydantic.BaseModel):
    address: str
    expiretm: TIMESTAMP_S
    new: typing.Optional[bool]


class _DepositAddressesResp(pydantic.BaseModel):

    # placeholder
    data: typing.Tuple[_DepositAddress, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint POST https://api.kraken.com/0/private/DepositAddresses

    Type: list of pydantic Models

    Model Fields:
    -------------
        address : str
            Deposit Address
        expiretm : float
            Expiration timestamp in seconds (0 if not expiring)
        new : bool
            Wether or not address has ever been used (optional)
    """

    def __call__(self, response: dict):
        _valid = _DepositAddressesResp(data=response)
        return _valid.data
        
    