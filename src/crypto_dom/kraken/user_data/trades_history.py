import typing
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import (
    TIMESTAMP_S,
    COUNT,
)
from crypto_dom.kraken.definitions import (
    ORDERID,
    TRADEID,
    ORDERTYPE,
    ORDERSIDE,
)


# ============================================================
# USER TRADES
# ============================================================


# doc: https://www.kraken.com/features/api#get-trades-history

URL = "https://api.kraken.com/0/private/TradesHistory"
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
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/private/TradesHistory

    Model Fields:
    -------------
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

    type: typing.Optional[
        Literal[
            "all", "any position", "closed position", "closing position", "no position"
        ]
    ]
    trades: typing.Optional[bool]
    start: typing.Optional[TIMESTAMP_S]
    end: typing.Optional[TIMESTAMP_S]
    ofs: typing.Optional[int]
    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
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


class _TradesHistoryResponse(pydantic.BaseModel):
    trades: typing.Mapping[TRADEID, _Trade]
    count: COUNT


#  this class is just to be consistent with our API
class Response(pydantic.BaseModel):
    """Response Model for endpoint https://api.kraken.com/0/private/TradesHistory

    Model Fields:
    -------------
        trades : dict
            Array of trade info with txid as the key
        count : int
            Amount of available trades info matching criteria

    Note:
    -----
        Trade Info dict type:
            ordertxid : str
                Order responsible for execution of trade
            pair : str
                Asset pair
            time : float
                Unix timestamp of trade in seconds
            type : Literal[buy, sell]
                Type of order (buy/sell)
            ordertype: str
                Order type
            price : Decimal
                Average price order was executed at (quote currency)
            cost : Decimal
                Total cost of order (quote currency)
            fee : Decimal
                Total fee (quote currency)
            vol : Decimal
                Volume (base currency)
            margin : Decimal
                Initial margin (quote currency)
            misc : List[str]
                Comma delimited list of miscellaneous info

        If the trade opened a position, the follow fields are also present in the trade info:

            posstatus : Literal[open, closed]
                Position status (open/closed)
            cprice : Decimal
                Average price of closed portion of position (quote currency)
            ccost : Decimal
                Total cost of closed portion of position (quote currency)
            cfee : Decimal
                Total fee of closed portion of position (quote currency)
            cvol : Decimal
                Total fee of closed portion of position (quote currency)
            cmargin : Decimal*
                Total margin freed in closed portion of position (quote currency)
            net : Decimal
                Net profit/loss of closed portion of position (quote currency, quote currency scale)
            trades : List[str]
                List of closing trades for position (if available)
    """

    def __call__(self, response: dict):
        return _TradesHistoryResponse(**response)
