import typing
from datetime import date
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from definitions import TIMEFRAMES, COUNT



# ============================================================
# ASSET PAIRS
# ============================================================


# doc: https://www.kraken.com/features/api#get-tradable-pairs 

URL = "https://api.kraken.com/0/public/AssetPairs"
METHOD = "GET"

# ------------------------------
# Request
# ------------------------------

class _AssetPairsReq(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/public/AssetPairs

    Fields:
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
    pair: typing.Optional[typing.List[str]]




# ------------------------------
# Response
# ------------------------------


def generate_model(keys: typing.List[str]) -> typing.Type[pydantic.BaseModel]:
    """dynamically create the model
    
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


    # TODO this should be enough for mypy
    _Sig = typing.Dict[str, _AssetPair]


    # we do not know the keys in advance, only the type of their value
    kwargs = {
        **{k: (_AssetPair, ...) for k in keys},
        "__base__": pydantic.BaseModel
    }

    model = pydantic.create_model(
        '_AssetPairsResp',
        **kwargs    #type: ignore
    )

    return model



class _AssetPairsResp:
    """Response Model for endpoint https://api.kraken.com/0/public/Trades

    Fields:
    -------
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

    """

    def __call__(self, **kwargs):
        model = generate_model(list(kwargs.keys()))
        print("\nFields", model.__fields__, "\n")
        return model(**kwargs)
