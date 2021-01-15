import typing
from datetime import date
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_S
from crypto_dom.kraken.definitions import TIMEFRAMES



# ============================================================
# OHLC
# ============================================================


# doc: https://www.kraken.com/features/api#get-ohlc-data

URL = "https://api.kraken.com/0/public/OHLC"
METHOD = "GET"


# ------------------------------
# Sample Response (ccxt)
# ------------------------------


#     {
#         "error":[],
#         "result":{
#             "XETHXXBT":[
#                 [1591475580,"0.02499","0.02499","0.02499","0.02499","0.00000","0.00000000",0],
#                 [1591475640,"0.02500","0.02500","0.02500","0.02500","0.02500","9.12201000",5],
#                 [1591475700,"0.02499","0.02499","0.02499","0.02499","0.02499","1.28681415",2],
#                 [1591475760,"0.02499","0.02499","0.02499","0.02499","0.02499","0.08800000",1],
#             ],
#             "last":1591517580
#         }
#     }


# ------------------------------
# Request
# ------------------------------

class _OhlcReq(pydantic.BaseModel):
    """Request model for endpoint https://api.kraken.com/0/public/OHLC"

    Fields:
    -------
        pair : str 
            Asset pair to get OHLC data for
        interval : int 
            Time frame interval in minutes (optional)
        since : float
            Return committed OHLC data since given id (optional)
    """

    pair: str
    interval: TIMEFRAMES = 1

    # timestamp in seconds
    since: typing.Optional[TIMESTAMP_S]

    @pydantic.validator('since')
    def check_year_from_timestamp(cls, v):
        if not v: return

        if v == 0: return v

        y = date.fromtimestamp(v).year
        if not y > 2009 and y < 2050:
            err_msg = f"Year {y} for timestamp {v} not within [2009, 2050]"
            raise ValueError(err_msg)
        return v


# ------------------------------
# Response
# ------------------------------

# TODO should this be a generic type instead ? ie _OhlcResp["XXBTZUSD"] instead of _OhlcResp("XXBTZUSD")
#       ? benefits for type hinting / mypy ??


def make_model_ohlc(pair: str) -> typing.Type[pydantic.BaseModel]:
    "dynamically create the model"
    

    class _BaseOhlcResp(pydantic.BaseModel):

        # timestamp received from kraken is in seconds
        last: TIMESTAMP_S

        @pydantic.validator('last', allow_reuse=True)
        def check_year_from_timestamp(cls, v):
            y = date.fromtimestamp(v).year
            if not y > 2009 and y < 2050:
                err_msg = f"Year {y} for timestamp {v} not within [2009, 2050]"
                raise ValueError(err_msg)
            return v

    # Entries(<time>, <open>, <high>, <low>, <close>, <vwap>, <volume>, <count>)
    _Candle = typing.Tuple[Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, int]

    kwargs = {
        pair: (
            # tuple : timestamp, open, high, low, close, vwap, volume, count
            typing.Tuple[_Candle, ...], ...
        ),
        "__base__": _BaseOhlcResp
    }

    model = pydantic.create_model(
        '_OhlcResp',
        **kwargs    #type: ignore
    )

    return model


#! GENERIC FOR TYPE HINTS == NOT WORKING YET 

Pair = typing.TypeVar("Pair")


class T_OhlcResp(typing.Generic[Pair]):

    def __init__(self, value: str):
        self._value = make_model_ohlc(value)

#! END ==================== 


class _OhlcResp:
    """Response model for endpoint https://api.kraken.com/0/public/OHLC"

    Fields:
    -------
        `pair_name` : str 
            Array of array entries(time, open, high, low, close, vwap, volume, count)
        last : int 
            id to be used as since when polling for new, committed OHLC data)
    """

    def __new__(_cls, pair: str):
        model = make_model_ohlc(pair)
        return model
