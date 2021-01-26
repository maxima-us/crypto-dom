import typing
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_S
from crypto_dom.kraken.definitions import ASSETCLASS, ASSET, KrakenID


# ============================================================
# DEPOSIT STATUS 
# ============================================================


# doc: https://www.kraken.com/features/api#deposit-status 

URL = "https://api.kraken.com/0/private/DepositStatus"
METHOD = "POST"


# ------------------------------
# Sample Response
# ------------------------------



# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint POST https://api.kraken.com/0/private/DepositStatus

    Model Fields:
    -------------
        aclass : str
            Default = currency (optional)
        asset : str enum
            Asset being deposited
        method : str
            Name of the deposit method
        nonce : int
            Always increasing unsigned 64 bit integer 
    """

    aclass: typing.Optional[ASSETCLASS]
    asset: ASSET
    method: str     # TODO this should be an enum
    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
# ------------------------------


class _DepositStatus(pydantic.BaseModel):
    method: str # TODO should be Literal
    aclass: ASSETCLASS
    asset: ASSET
    refid: str
    txid: KrakenID  # FIXME verify
    info: str   # FIXME verify
    amount: Decimal
    fee: Decimal
    time: TIMESTAMP_S
    status: str # FIXME verify and should probably also be a LIteral
    status_prop: typing.Optional[Literal["return", "onhold"]] = pydantic.Field(alias="status-prop")


class _DepositStatusResp(pydantic.BaseModel):

    # placeholder
    data: typing.Tuple[_DepositStatus, ...]

#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint POST https://api.kraken.com/0/private/DepositStatus

    Type: array of pydantic Model

    Model Fields:
    -------------
        method : str enum
            Name of the deposit method used
        aclass : str
            Asset class
        asset : str enum
            Asset X-ISO4217-A3 code
        refid : str
            Reference id
        txid : str
            Method transaction id
        info : str
            Method transaction information
        amount : Decimal
            Amount deposited
        fee : Decimal
            Fees paid
        time : float
            Timestam in seconds when request was made
        status : str enum
            Status of deposit
        status-prop : str enum
            Additional status properties (if available)
            return = a return transaction initiated by Kraken
            onhold = deposit is on hold pending review
    """

    def __call__(self, response: dict):
        _valid = _DepositStatusResp(data=response)
        return _valid.data
        
    