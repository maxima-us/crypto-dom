import typing
from datetime import date
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from definitions import TIMEFRAMES, COUNT



# ============================================================
# OHLC
# ============================================================


# doc: https://www.kraken.com/features/api#get-recent-trades 

URL = "https://api.kraken.com/0/public/Trades"
METHOD = "GET"

# ------------------------------
# Request
# ------------------------------

class _TradesReq(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/public/Trades

    Fields:
    -------
        pair : str 
            Asset pair to get OHLC data for
        since : int 
            Return trade data since given id (optional)
    """

    pair: str
    since: typing.Optional[pydantic.PositiveInt]

    @pydantic.validator('since')
    def check_year_from_timestamp(cls, v):
        if v == 0 or v is None:
            return v

        # convert from ns to s
        v_s = v * 10**-9

        y = date.fromtimestamp(v_s).year
        if not y > 2009 and y < 2050:
            err_msg = f"Year {y} for timestamp {v} not within [2009, 2050]"
            raise ValueError(err_msg)
        return v


# ------------------------------
# Response
# ------------------------------


def generate_model(pair: str) -> typing.Type[pydantic.BaseModel]:
    "dynamically create the model"


    class _BaseTradesResp(pydantic.BaseModel):

        # timestamp received from kraken in ns
        last: pydantic.PositiveInt

        @pydantic.validator('last')
        def check_year_from_timestamp(cls, v, values):
            # convert from ns to s
            v_s = v * 10**-9

            y = date.fromtimestamp(v_s).year
            if not y > 2009 and y < 2050:
                err_msg = f"Year {y} for timestamp {v} not within [2009, 2050]"
                raise ValueError(err_msg)
            return v

    _Trade = typing.Tuple[Decimal, Decimal, Decimal, Literal["b", "s"], Literal["m", "l"], typing.Any]

    kwargs = {
        pair: (typing.Tuple[_Trade, ...], ...),
        "__base__": _BaseTradesResp
    }

    model = pydantic.create_model(
        '_TradesResp',
        **kwargs    #type: ignore
    )

    return model



class _TradesResp:
    """Response Model for endpoint https://api.kraken.com/0/public/Trades

    Fields:
    -------
        `pair_name` : str
            Array of array entries(price, volume, time, buy/sell, market/limit, miscellaneous)
        last: int
            Id to be used as since when polling for new trade dat
    """

    def __new__(_cls, pair: str):
        print("calling new")
        model = generate_model(pair)
        return model
