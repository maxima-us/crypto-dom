import typing
from datetime import date
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")



# ============================================================
# TICKER
# ============================================================


# doc: https://www.kraken.com/features/api#get-ticker-info

URL = "https://api.kraken.com/0/public/Ticker"
METHOD = "GET"

# ------------------------------
# Request
# ------------------------------

class _TickerReq(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/public/Ticker

    Fields:
    -------
        pair : List[str]
            comma delimited list of asset pairs to get info on (optional)
            default = all
    """

    pair: typing.Optional[typing.List[str]]



# ------------------------------
# Response
# ------------------------------


def generate_model(keys: typing.List[str]) -> typing.Type[pydantic.BaseModel]:
    """dynamically create the model
    
    Args:
    ----
        key: List[str]
            List of assetpair names that map to their ticker info

    """


    class _Ticker(pydantic.BaseModel):

        a: typing.Tuple[Decimal, Decimal, Decimal]
        b: typing.Tuple[Decimal, Decimal, Decimal]
        c: typing.Tuple[Decimal, Decimal]
        v: typing.Tuple[Decimal, Decimal]
        p: typing.Tuple[Decimal, Decimal]
        t: typing.Tuple[Decimal, Decimal]
        l: typing.Tuple[Decimal, Decimal]
        h: typing.Tuple[Decimal, Decimal]
        o: Decimal


    # we do not know the keys in advance, only the type of their value
    kwargs = {
        **{k: (_Ticker, ...) for k in keys},
        "__base__": pydantic.BaseModel
    }

    model = pydantic.create_model(
        '_TickerResp',
        **kwargs    #type: ignore
    )

    return model



class _TickerResp:
    """Response Model for endpoint https://api.kraken.com/0/public/Ticker

    Fields:
    -------
        `pair_name` : dict
            Array of pair name and corresponding info
                a = ask array(<price>, <whole lot volume>, <lot volume>),
                b = bid array(<price>, <whole lot volume>, <lot volume>),
                c = last trade closed array(<price>, <lot volume>),
                v = volume array(<today>, <last 24 hours>),
                p = volume weighted average price array(<today>, <last 24 hours>),
                t = number of trades array(<today>, <last 24 hours>),
                l = low array(<today>, <last 24 hours>),
                h = high array(<today>, <last 24 hours>),
                o = today's opening price 

    """

    def __call__(self, **kwargs):
        model = generate_model(list(kwargs.keys()))
        print("\nFields", model.__fields__, "\n")
        return model(**kwargs)
