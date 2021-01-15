import typing
from datetime import date
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.kraken.definitions import (
    TIMEFRAMES,
    TIMESTAMP_S,
    COUNT
)



# ============================================================
# ACCOUNT BALANCES
# ============================================================


# doc: https://www.kraken.com/features/api#get-account-balance 

URL = "https://api.kraken.com/0/public/Balance"
METHOD = "GET"

# ------------------------------
# Request
# ------------------------------

class _AccountBalanceReq(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/public/Balance

    Fields:
    -------
        nonce: int
            Always increasing unsigned 64 bit integer
    """

    nonce: pydantic.PositiveInt




# ------------------------------
# Response
# ------------------------------


def generate_model(keys: typing.List[str]) -> typing.Type[pydantic.BaseModel]:
    "dynamically create the model"


    kwargs = {
        **{k: (Decimal, ...) for k in keys},
        "__base__": pydantic.BaseModel
    }

    model = pydantic.create_model(
        '_AssetsResp',
        **kwargs    #type: ignore
    )

    return model



class _AccountBalanceResp:
    """Response Model for endpoint https://api.kraken.com/0/public/Balance

    Fields:
    -------
        `asset name` : Decimal
            Array of asset name and corresponding balance amount
    """

    def __call__(self, **kwargs):
        model = generate_model(list(kwargs.keys()))
        print("\nFields", model.__fields__, "\n")
        return model(**kwargs)
