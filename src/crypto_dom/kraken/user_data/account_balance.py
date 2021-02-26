import typing
from datetime import date
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter

stackprinter.set_excepthook(style="darkbg2")


# ============================================================
# ACCOUNT BALANCES
# ============================================================


# doc: https://www.kraken.com/features/api#get-account-balance

URL = "https://api.kraken.com/0/private/Balance"
METHOD = "POST"


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/private/Balance

    Model Fields:
    -------------
        nonce: int
            Always increasing unsigned 64 bit integer
    """

    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
# ------------------------------


def _generate_model(keys: typing.List[str]) -> typing.Type[pydantic.BaseModel]:
    "dynamically create the model. Returns new pydantic model class"

    kwargs = {**{k: (Decimal, ...) for k in keys}, "__base__": pydantic.BaseModel}

    model = pydantic.create_model("_AccountBalanceResponse", **kwargs)  # type: ignore

    return model


class Response:
    """Response Model for endpoint https://api.kraken.com/0/private/Balance

    Model Fields:
    -------------
        `asset name` : Decimal
            Array of asset name and corresponding balance amount
    """

    def __call__(self, response: dict):
        model = _generate_model(list(response.keys()))
        # print("\nFields", model.__fields__, "\n")
        return model(**response)
