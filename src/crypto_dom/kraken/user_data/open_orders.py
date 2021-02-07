import typing
from decimal import Decimal

import pydantic
import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_S
from crypto_dom.kraken.definitions import (
    FLAGS,
    ORDERSIDE,
    ORDERTYPE,
    ORDERSTATUS,
    ORDERID,
)


# ============================================================
# OPEN ORDERS
# ============================================================


# doc: https://www.kraken.com/features/api#get-open-orders

URL = "https://api.kraken.com/0/private/OpenOrders"
METHOD = "POST"


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/private/OpenOrders

    Model Fields:
    -------------
        trades : bool
            Whether or not to include trades in output (optional)
                default = false
        userref : int
            Restrict results to given user reference id (optional)
        nonce: int
            Always increasing unsigned 64 bit integer

    """

    trades: typing.Optional[bool]
    userref: typing.Optional[int]
    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
# ------------------------------


class _Descr(pydantic.BaseModel):

    pair: str  # different format than assetpairs keys (see example: ETHUSDT vs XETHZUSD)
    type: ORDERSIDE
    ordertype: ORDERTYPE
    price: Decimal
    leverage: str  # will be of format "5:1"
    order: str
    close: typing.Union[str, Decimal]


class _OpenOrder(pydantic.BaseModel):

    refid: typing.Optional[str]  # references order ID (string)
    userref: typing.Optional[int]
    status: ORDERSTATUS
    opentm: TIMESTAMP_S
    starttm: TIMESTAMP_S
    expiretm: TIMESTAMP_S
    descr: _Descr
    vol: Decimal
    vol_exec: Decimal
    cost: Decimal
    fee: Decimal
    price: Decimal
    stopprice: Decimal
    limitprice: Decimal
    misc: typing.Any
    oflags: FLAGS


class _OpenOrdersResponse(pydantic.BaseModel):

    open: typing.Mapping[ORDERID, _OpenOrder]


#  this class is just to be consistent with our API
class Response(pydantic.BaseModel):
    """Response Model for endpoint https://api.kraken.com/0/private/OpenOrders

    Model Fields:
    -------------
        open: dict
            mapping of txid to their order info
                txid : str
                order info : dict

    Note:
    -----
        Order Info dict type
            refid : str
                Referral order transaction id that created this order
            userref : int
                User reference id
            status : Literal[pending, open, closed, canceled, expired]
                Status of order:
            opentm : int
                Snix timestamp (in seconds) of when order was placed
            starttm : int
                Unix timestamp (in seconds) of order start time (or 0 if not set)
            expiretm : int
                Unix timestamp (in seconds) of order end time (or 0 if not set)
            descr : dict
                order description info
                    pair = asset pair
                    type = type of order (buy/sell)
                    ordertype = order type (See Add standard order)
                    price = primary price
                    price2 = secondary price
                    leverage = amount of leverage
                    order = order description
                    close = conditional close order description (if conditional close set)
            vol : Decimal
                Volume of order (base currency unless viqc set in oflags)
            vol_exec : Decimal
                Volume executed (base currency unless viqc set in oflags)
            cost : Decimal
                Total cost (quote currency unless unless viqc set in oflags)
            fee : Decimal
                Total fee (quote currency)
            price : Decimal
                Average price (quote currency unless viqc set in oflags)
            stopprice : Decimal
                Stop price (quote currency, for trailing stops)
            limitprice : Decimal
                Triggered limit price (quote currency, when limit based order type triggered)
            misc : List[Any]
                Comma delimited list of miscellaneous info
                    stopped = triggered by stop price
                    touched = triggered by touch price
                    liquidated = liquidation
                    partial = partial fill
            oflags : List[Literal[viqc, fcib, fciq, nompp]]
                Comma delimited list of order flags
                    viqc = volume in quote currency
                    fcib = prefer fee in base currency (default if selling)
                    fciq = prefer fee in quote currency (default if buying)
                    nompp = no market price protection
            trades : List[str]
                Array of trade ids related to order (if trades info requested and data available)
    """

    def __call__(self, response: dict):
        return _OpenOrdersResponse(**response)
