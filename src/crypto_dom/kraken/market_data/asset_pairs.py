import typing
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import COUNT
from crypto_dom.kraken.definitions import PAIR


# ============================================================
# ASSET PAIRS
# ============================================================


# doc: https://www.kraken.com/features/api#get-tradable-pairs

URL = "https://api.kraken.com/0/public/AssetPairs"
METHOD = "GET"


# ------------------------------
# Sample Response
# ------------------------------


#     {
#         "error":[],
#         "result":{
#             "ADAETH":{
#                 "altname":"ADAETH",
#                 "wsname":"ADA\/ETH",
#                 "aclass_base":"currency",
#                 "base":"ADA",
#                 "aclass_quote":"currency",
#                 "quote":"XETH",
#                 "lot":"unit",
#                 "pair_decimals":7,
#                 "lot_decimals":8,
#                 "lot_multiplier":1,
#                 "leverage_buy":[],
#                 "leverage_sell":[],
#                 "fees":[
#                     [0,0.26],
#                     [50000,0.24],
#                     [100000,0.22],
#                     [250000,0.2],
#                     [500000,0.18],
#                     [1000000,0.16],
#                     [2500000,0.14],
#                     [5000000,0.12],
#                     [10000000,0.1]
#                 ],
#                 "fees_maker":[
#                     [0,0.16],
#                     [50000,0.14],
#                     [100000,0.12],
#                     [250000,0.1],
#                     [500000,0.08],
#                     [1000000,0.06],
#                     [2500000,0.04],
#                     [5000000,0.02],
#                     [10000000,0]
#                 ],
#                 "fee_volume_currency":"ZUSD",
#                 "margin_call":80,
#                 "margin_stop":40,
#                 "ordermin": "1"
#             },
#         }
#     }
#


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/public/AssetPairs

    Model Fields:
    -------
        info : Literal["info", "leverage", "fees"]
            info to retrieve (optional)
                info = all info (default)
                leverage = leverage info
                fees = fees schedule
        pair : List[str]
            comma delimited list of asset pairs to get info on (optional)
            default = all
    """

    info: Literal["info", "leverage", "fees"]
    pair: typing.Optional[typing.List[PAIR]]


# ------------------------------
# Response Model
# ------------------------------


def _generate_model(keys: typing.List[str]) -> typing.Type[pydantic.BaseModel]:
    """dynamically create the model. Returns a new pydantic model class

    Args:
    ----
        key: List[str]
            List of assetpair names that map to their info

    """

    class _AssetPair(pydantic.BaseModel):

        altname: str
        # darkpools don't have a wsname
        wsname: typing.Optional[str]
        # TODO should strings always be StrictStr
        aclass_base: str
        base: str
        aclass_quote: str
        quote: str
        lot: str
        pair_decimals: COUNT
        lot_decimals: COUNT
        lot_multiplier: COUNT
        leverage_buy: typing.Tuple[int, ...]
        leverage_sell: typing.Tuple[int, ...]
        fees: typing.Tuple[typing.Tuple[Decimal, Decimal], ...]
        fees_maker: typing.Tuple[typing.Tuple[Decimal, Decimal], ...]
        fee_volume_currency: str
        margin_call: pydantic.PositiveInt
        margin_stop: pydantic.PositiveInt
        ordermin: typing.Optional[Decimal]

    # we do not know the keys in advance, only the type of their value
    kwargs = {**{k: (_AssetPair, ...) for k in keys}, "__base__": pydantic.BaseModel}

    model = pydantic.create_model("_AssetPairsResponse", **kwargs)  # type: ignore

    return model


class Response:
    """Response Model for endpoint https://api.kraken.com/0/public/AssetPairs

    Model Fields:
    -------------
        `pair_name` : dict
            Array of pair name and corresponding info
                altname = alternate pair name
                wsname = WebSocket pair name (if available)
                aclass_base = asset class of base component
                base = asset id of base component
                aclass_quote = asset class of quote component
                quote = asset id of quote component
                lot = volume lot size
                pair_decimals = scaling decimal places for pair
                lot_decimals = scaling decimal places for volume
                lot_multiplier = amount to multiply lot volume by to get currency volume
                leverage_buy = array of leverage amounts available when buying
                leverage_sell = array of leverage amounts available when selling
                fees = fee schedule array in [volume, percent fee] tuples
                fees_maker = maker fee schedule array in [volume, percent fee] tuples (if on maker/taker)
                fee_volume_currency = volume discount currency
                margin_call = margin call level
                margin_stop = stop-out/liquidation margin level
                ordermin = minimum order volume for pair

    Usage:
    ------
        model = Response()
        validated_response = model(JSON_response_content)
    """

    def __call__(self, response: dict):
        model = _generate_model(list(response.keys()))
        # print("\nFields", model.__fields__, "\n")
        return model(**response)
