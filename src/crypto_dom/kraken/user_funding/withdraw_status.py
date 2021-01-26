import typing
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_S
from crypto_dom.kraken.definitions import ASSETCLASS, ASSET, KrakenID


# ============================================================
# WITHDRAWAL STATUS
# ============================================================


# doc: https://www.kraken.com/features/api#withdraw-status

URL = "https://api.kraken.com/0/private/WithdrawStatus"
METHOD = "POST"


# ------------------------------
# Sample Response
# ------------------------------



# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint POST https://api.kraken.com/0/private/WithdrawStatus

    Model Fields:
    -------------
        aclass : str
            Default = currency (optional)
        asset : str enum
            Asset being withdrawn
        method : str enum
            Withdrawal method name (optional)
        nonce : int
            Always increasing unsigned 64 bit integer 
    """

    aclass: typing.Optional[ASSETCLASS]
    asset: ASSET
    method: typing.Optional[str] # TODO str enum

    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
# ------------------------------


class _WithdrawStatus(pydantic.BaseModel):
    method: str # TODO should be Literal
    aclass: ASSETCLASS
    asset: ASSET
    refid: str
    txid: KrakenID
    info: str
    amount: Decimal
    fee: Decimal
    time: TIMESTAMP_S
    status: str
    status_prop: typing.Optional[Literal["cancel-pending", "canceled", "cancel-denied", "return", "onhold"]] = pydantic.Field(alias="status-prop")


class _WithdrawStatusResp(pydantic.BaseModel):
    
    #placeholder
    data: typing.Tuple[_WithdrawStatus, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint POST https://api.kraken.com/0/private/WithdrawStatus

    Type: array of pydantic Model

    Model Fields:
    -------------
        method : str enum
            Name of withdrawal medthod used
        aclass : str
            Asset Class
        asset : str
            Asset 
        refid : str
            Reference Id
        txid : str
            Method transaction id
        info : str
            Method transaction info
        amount : Decimal
            Amount withdrawn
        fee : Decimal
            Fees paid
        time : float
            Timestamp in seconds when request was made
        status : str enum
            Status of withdrawal
        status-prop : str enum
            Additional status properties (if available)
            cancel-pending = cancelation requested
            canceled = canceled
            cancel-denied = cancelation requested but was denied
            return = a return transaction initiated by Kraken; it cannot be canceled
            onhold = withdrawal is on hold pending review
    """

    def __call__(self, response: dict):
        _valid = _WithdrawStatusResp(data=response)
        return _valid.data
    