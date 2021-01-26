from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.kraken.definitions import ASSETCLASS, ASSET


# ============================================================
# WALLET TRANSFER
# ============================================================


# doc: https://www.kraken.com/features/api#wallet-transfer

URL = "https://api.kraken.com/0/private/WalletTransfer"
METHOD = "POST"


# ------------------------------
# Sample Response
# ------------------------------



# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint POST https://api.kraken.com/0/private/WalletTransfer

    Model Fields:
    -------------
        asset : str enum
            Asset being withdrawn
        to : str
            Which wallet the funds are being transferred to
            Default = Futures Wallet
        from : str
            Which wallet the funds are being transferred from
            Default = Spot Wallet
        amount : Decimal
            Amount to withdraw, including fees
        nonce : int
            Always increasing unsigned 64 bit integer 
    """

    asset: ASSET
    to: str
    _from: str = pydantic.Field(alias="from")
    amount: Decimal
    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
# ------------------------------


class _WalletTransferResp(pydantic.BaseModel):
    refid: str 


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint POST https://api.kraken.com/0/private/WalletTransfer

    Type: pydantic Model

    Model Fields:
    -------------
        refid: str
            Reference id

    """

    def __call__(self, response: dict):
        return _WalletTransferResp(response)