import typing
from datetime import date
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from definitions import (
    TIMEFRAMES,
    TIMESTAMP_S,
    COUNT,
    ORDERID,
    TRADEID,
    ORDERSTATUS,
    ORDERTYPE,
    ORDERSIDE,
    FLAGS
)



# ============================================================
# USER TRADES
# ============================================================


# doc: https://www.kraken.com/features/api#get-trades-history

URL = "https://api.kraken.com/0/public/TradesHistory"
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

class _TradesHistoryReq(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/public/TradesHistory

    Fields:
    -------
        type : Literal[all, any position, closed position, closing position, no position]
            type of trade (optional)
                default = all
        trades: bool
            Whether or not to include trades in output (optional)
                default = false
        start : int
            Starting unix timestamp (in seconds) or order tx id of results (optional)
        end : int
            Ending unix timestamp (in seconds) or order tx id of results (optional)
        ofs : int 
            Result offset
        nonce: int
            Always increasing unsigned 64 bit integer
    """

    type: typing.Optional[Literal["all", "any position", "closed position", "closing position", "no position"]]
    trades: typing.Optional[bool]
    start: typing.Optional[TIMESTAMP_S]
    end: typing.Optional[TIMESTAMP_S]
    ofs: typing.Optional[int]
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


class _TradesHistory(pydantic.BaseModel):
    trades: typing.Mapping[TRADEID, _Trade]
    count: COUNT


#  this class is just to be consistent with our API
# TODO fill fields in docstring
class _TradesHistoryResp(pydantic.BaseModel):
    """Response Model for endpoint https://api.kraken.com/0/public/TradesHistory

    Fields:
    -------
   """

    def __new__(cls):
        return _TradesHistory


