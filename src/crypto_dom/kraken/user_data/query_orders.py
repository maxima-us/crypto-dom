import typing
from decimal import Decimal

import pydantic
import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_S
from crypto_dom.kraken.definitions import (
    ORDERID,
    ORDERSTATUS,
    ORDERTYPE,
    ORDERSIDE,
    FLAGS,
)


# ============================================================
# QUERY ORDERS INFO
# ============================================================


# doc: https://www.kraken.com/features/api#query-orders-info

URL = "https://api.kraken.com/0/private/QueryOrders"
METHOD = "POST"


# ------------------------------
# Sample Response (ccxt)
# ------------------------------


#     {
#         "error":[],
#         "result":{
#             "OTLAS3-RRHUF-NDWH5A":{
#                 "refid":null,
#                 "userref":null,
#                 "status":"closed",
#                 "reason":null,
#                 "opentm":1586822919.3342,
#                 "closetm":1586822919.365,
#                 "starttm":0,
#                 "expiretm":0,
#                 "descr":{
#                     "pair":"XBTUSDT",
#                     "type":"sell",
#                     "ordertype":"market",
#                     "price":"0",
#                     "price2":"0",
#                     "leverage":"none",
#                     "order":"sell 0.21804000 XBTUSDT @ market",
#                     "close":""
#                 },
#                 "vol":"0.21804000",
#                 "vol_exec":"0.21804000",
#                 "cost":"1493.9",
#                 "fee":"3.8",
#                 "price":"6851.5",
#                 "stopprice":"0.00000",
#                 "limitprice":"0.00000",
#                 "misc":"",
#                 "oflags":"fciq",
#                 "trades":["TT5UC3-GOIRW-6AZZ6R"]
#             }
#         }
#     }


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/private/QueryOrders

    Model Fields:
    -------------
        trades: bool
            Whether or not to include trades in output (optional)
                default = false
        userref : int
            Restrict results to given user reference id (optional)
        txid : List[str]
            Comma delimited list of transaction ids to query info about (50 maximum)
        nonce: int
            Always increasing unsigned 64 bit integer
    """

    trades: bool
    userref: typing.Optional[int]
    txid: typing.List[ORDERID]
    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
# ------------------------------


def _generate_model(keys: typing.List[ORDERID]) -> typing.Type[pydantic.BaseModel]:
    "dynamically create the model. Returns a new pydantic model class"

    class _Descr(pydantic.BaseModel):
        pair: str  # not necessarily of the same format as assetpairs keys
        type: ORDERSIDE
        ordertype: ORDERTYPE
        price: Decimal
        leverage: str  # will be of format "5:1"
        order: str
        close: typing.Union[str, Decimal]

    class _ClosedOrder(pydantic.BaseModel):

        #  shared with open order info
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

        # in addition to open order info
        closetm: typing.Optional[TIMESTAMP_S]
        reason: typing.Optional[str]

    # we do not know the keys in advance, only the type of their value
    kwargs = {**{k: (_ClosedOrder, ...) for k in keys}, "__base__": pydantic.BaseModel}

    model = pydantic.create_model("_QueryOrdersResponse", **kwargs)  # type: ignore

    return model


# TODO fill fields in docstring
class Response(pydantic.BaseModel):
    """Response Model for endpoint https://api.kraken.com/0/public/QueryOrders

    Model Fields:
    -------
    """

    def __call__(self, response: dict):
        model = _generate_model(list(response.keys()))
        # print("\nFields", model.__fields__, "\n")
        return model(**response)
