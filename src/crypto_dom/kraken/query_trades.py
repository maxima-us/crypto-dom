import typing
from datetime import date
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_S, COUNT
from crypto_dom.kraken.definitions import (
    ORDERID,
    TRADEID,
    ORDERTYPE,
    ORDERSIDE,
)



# ============================================================
# QUERY TRADES
# ============================================================


# doc: https://www.kraken.com/features/api#query-trades-info 

URL = "https://api.kraken.com/0/public/QueryTrades"
METHOD = "POST"


# ------------------------------
# Sample Response (ccxt)
# ------------------------------


#     {
#         "error": [],
#         "result": {
#             "trades": {
#                 "GJ3NYQ-XJRTF-THZABF": {
#                     "ordertxid": "TKH2SE-ZIF5E-CFI7LT",
#                     "postxid": "OEN3VX-M7IF5-JNBJAM",
#                     "pair": "XICNXETH",
#                     "time": 1527213229.4491,
#                     "type": "sell",
#                     "ordertype": "limit",
#                     "price": "0.001612",
#                     "cost": "0.025792",
#                     "fee": "0.000026",
#                     "vol": "16.00000000",
#                     "margin": "0.000000",
#                     "misc": ""
#                 },
#                 ...
#             },
#             "count": 9760,
#         },
#     }


# ------------------------------
# Request
# ------------------------------

class _QueryTradesReq(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/public/QueryTrades

    Fields:
    -------
        txid : List[str]
            Comma delimited list of transaction ids to query info about (20 maximum)
        trades: bool
            Whether or not to include trades in output (optional)
                default = false
        nonce: int
            Always increasing unsigned 64 bit integer
    """
    txid: typing.List[TRADEID]
    trades: typing.Optional[bool]
    nonce: pydantic.PositiveInt


# ------------------------------
# Response
# ------------------------------


class _Trade(pydantic.BaseModel):
    ordertxid: ORDERID
    postxid: TRADEID
    pair: str
    time: TIMESTAMP_S
    type: ORDERSIDE 
    ordertype: ORDERTYPE
    price: Decimal
    cost: Decimal
    fee: Decimal
    vol: Decimal
    margin: Decimal
    misc: typing.Any

    # If the trade opened a position, the follow fields are also present in the trade info:
    posstatus: typing.Optional[Literal["open", "closed"]]
    cprice: typing.Optional[Decimal]
    ccost: typing.Optional[Decimal]
    cfee: typing.Optional[Decimal]
    cvol: typing.Optional[Decimal]
    cmargin: typing.Optional[Decimal]
    cnet: typing.Optional[typing.Tuple[Decimal, Decimal]]
    trades: typing.Optional[typing.Tuple[typing.Any, ...]]


class _QueryTrades(pydantic.BaseModel):
    trades: typing.Mapping[TRADEID, _Trade]
    count: COUNT


#  this class is just to be consistent with our API
# TODO fill fields in docstring
class _QueryTradesResp(pydantic.BaseModel):
    """Response Model for endpoint https://api.kraken.com/0/public/QueryTrades

    Fields:
    -------
   """

    def __new__(cls):
        return _QueryTrades


