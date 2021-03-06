import typing
from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.kraken.definitions import ASSETCLASS, ASSET


# ============================================================
# DEPOSIT METHODS 
# ============================================================


# doc: https://www.kraken.com/features/api#deposit-methods 

URL = "https://api.kraken.com/0/private/DepositMethods"
METHOD = "POST"


# ------------------------------
# Sample Response
# ------------------------------


#[
# {
#   'fee': '0.0000000000', 
#   'gen-address': True, 
#   'limit': False, 
#   'method': 'Ether (Hex)'
#  }
# ]


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint POST https://api.kraken.com/0/private/DepositMethods

    Model Fields:
    -------------
        aclass : str
            Default = currency (optional)
        asset : str enum
            Asset being deposited
        nonce : int
            Always increasing unsigned 64 bit integer 
    """

    aclass: typing.Optional[ASSETCLASS]
    asset: ASSET
    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
# ------------------------------


class _Method(pydantic.BaseModel):
    method: str     # TODO should be Literal
    limit: typing.Union[Decimal, bool]
    fee: Decimal
    address_setup_fee: typing.Optional[bool] = pydantic.Field(alias="address-setup-fee")


class _DepositMethodsResponse(pydantic.BaseModel):

    # placeholder
    data: typing.Tuple[_Method, ...]




#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint POST https://api.kraken.com/0/private/DepositMethods

    Type: list of pydantic models

    Model Fields:
    -------------
        method : str enum
            Name of deposit method
        limit : Union[Decimal, bool]
            Maximum net amount that can be deposited right now, or false if no limit
        fee: Decimal
        address-setup-fee: bool
            whether or not method has an address setup fee (optional)
    """

    def __call__(self, response: dict):
        _valid = _DepositMethodsResponse(data=response)
        return _valid.data
        
    