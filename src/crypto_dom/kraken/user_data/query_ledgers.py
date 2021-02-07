import typing
from decimal import Decimal

import pydantic
import stackprinter

stackprinter.set_excepthook(style="darkbg2")  # type: ignore

from crypto_dom.definitions import TIMESTAMP_S
from crypto_dom.kraken.definitions import LEDGERID, ASSET


# ============================================================
# QUERY LEDGERS
# ============================================================


# doc: https://www.kraken.com/features/api#query-ledgers

URL = "https://api.kraken.com/0/public/QueryLedgers"
METHOD = "POST"


# ------------------------------
# Sample Response (ccxt)
# ------------------------------


# { error: [],
#   result: {'LPUAIB-TS774-UKHP7X': {  refid: "A2B4HBV-L4MDIE-JU4N3N",
#                                         time:  1520103488.314,
#                                         type: "withdrawal",
#                                       aclass: "currency",
#                                        asset: "XETH",
#                                       amount: "-0.2805800000",
#                                          fee: "0.0050000000",
#                                      balance: "0.0000051000"           }}}


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/public/QueryLedgers

    Model Fields:
    -------------
        id : List[str]
            Comma delimited list of ledger ids to query info about (20 maximum)
        nonce : int
            Always increasing unsigned 64 bit integer
    """

    id: typing.List[LEDGERID]
    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
# ------------------------------


def _generate_model(keys: typing.List[LEDGERID]) -> typing.Type[pydantic.BaseModel]:
    "dynamically create the model. Returns a new pydantic model class"

    class _Ledger(pydantic.BaseModel):

        refid: typing.Optional[str]  # TODO is this also in the KrakenID format ??
        time: TIMESTAMP_S
        type: str
        aclass: str
        asset: ASSET
        amount: Decimal
        fee: Decimal
        balance: Decimal

    # we do not know the keys in advance, only the type of their value
    kwargs = {**{k: (_Ledger, ...) for k in keys}, "__base__": pydantic.BaseModel}

    model = pydantic.create_model("_QueryLedgersResponse", **kwargs)  # type: ignore

    return model


class Response(pydantic.BaseModel):
    """Response Model for endpoint https://api.kraken.com/0/public/QueryLedgers

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
        model = _generate_model(list(response.keys()))
        # print("\nFields", model.__fields__, "\n")
        return model(**response)
