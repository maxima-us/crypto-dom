import typing
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_S
from crypto_dom.kraken.definitions import ORDERID


# ============================================================
# LEDGERS
# ============================================================


# doc: https://www.kraken.com/features/api#get-ledgers-info

URL = "https://api.kraken.com/0/public/Ledgers"
METHOD = "POST"


# ------------------------------
# Sample Response (ccxt)
# ------------------------------


# { error: [],
#   result: {ledger: {'LPUAIB-TS774-UKHP7X': {  refid: "A2B4HBV-L4MDIE-JU4N3N",
#                                                   time:  1520103488.314,
#                                                   type: "withdrawal",
#                                                 aclass: "currency",
#                                                  asset: "XETH",
#                                                 amount: "-0.2805800000",
#                                                    fee: "0.0050000000",
#                                                balance: "0.0000051000"


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/public/Ledgers

    Fields:
    -------
         aclass : str
            Asset Class (optional)
                currency (default)
        asset : str
            Comma delimited list of assets to restrict output to (optional)
                default = all
        type : Literal[all, deposit, withdrawal, trade, margin]
            Type of ledger to retrieve (optional)
                default = all
        start : int
            Starting unix timestamp (in seconds) or ledger id of results (optional)
        end : int
            Ending unix timestamp (in seconds) or ledger id of results (optional)
        ofs : int
            Result offset
        nonce: int
            Always increasing unsigned 64 bit integer
    """

    aclass: typing.Optional[str]
    asset: typing.Optional[typing.List[str]]
    type: typing.Optional[Literal["all", "deposit", "withdraw", "trade", "margin"]]
    start: typing.Optional[TIMESTAMP_S]
    end: typing.Optional[TIMESTAMP_S]
    ofs: typing.Optional[int]
    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
# ------------------------------


def generate_model(keys: typing.List[ORDERID]) -> typing.Type[pydantic.BaseModel]:
    "dynamically create the model"

    class _Ledger(pydantic.BaseModel):

        refid: typing.Optional[str]
        time: TIMESTAMP_S
        type: str
        aclass: str
        asset: str
        amount: Decimal
        fee: Decimal
        balance: Decimal

    # we do not know the keys in advance, only the type of their value
    kwargs = {**{k: (_Ledger, ...) for k in keys}, "__base__": pydantic.BaseModel}

    model = pydantic.create_model("_LedgersResponse", **kwargs)  # type: ignore

    return model


class Response(pydantic.BaseModel):
    """Response Model for endpoint https://api.kraken.com/0/public/Ledgers

    Model Fields:
    -------------
        `Ledger id` : leger info
            mapping of ledger id to their info
                ledger id : str
                ledger info : dict

    Note:
    -----
        Ledger Info dict type:
            refid: str
                Reference id
            time : float
                Unix timestamp of ledger in seconds
            type : str
                Type of ledger entry
            aclass : str
                Asset class
            asset : str
                Asset
            amount : Decimal
                Transaction amount
            fee : Decimal
                Transaction fee
            balance : Decimal
                Resulting balance
    """

    def __call__(self, response: dict):
        model = generate_model(list(response.keys()))
        # print("\nFields", model.__fields__, "\n")
        return model(**response)
