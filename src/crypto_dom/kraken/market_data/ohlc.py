import typing
from datetime import date
from decimal import Decimal

import pydantic
import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_S
from crypto_dom.kraken.definitions import TIMEFRAME, PAIR


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
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint https://api.kraken.com/0/public/OHLC"

    Model Fields:
    -------
        pair : str
            Asset pair to get OHLC data for
        interval : int
            Time frame interval in minutes (optional)
        since : float
            Return committed OHLC data since given id (optional)
    """

    pair: PAIR
    interval: typing.Optional[TIMEFRAME]

    # timestamp in seconds
    since: typing.Optional[TIMESTAMP_S]

    @pydantic.validator("since")
    def check_year_from_timestamp(cls, v):
        if not v:
            return

        if v == 0:
            return v

        y = date.fromtimestamp(v).year
        if not y > 2009 and y < 2050:
            err_msg = f"Year {y} for timestamp {v} not within [2009, 2050]"
            raise ValueError(err_msg)
        return v


# ------------------------------
# Response Model
# ------------------------------


# TODO should this be a generic type instead ? ie _OhlcResp["XXBTZUSD"] instead of _OhlcResp("XXBTZUSD")
#       ? benefits for type hinting / mypy ??


def _generate_model(pair: str) -> typing.Type[pydantic.BaseModel]:
    "dynamically create the model. Returns a new pydantic model class"

    # TODO put in validators.py
    class _BaseOhlcResp(pydantic.BaseModel):

        # timestamp received from kraken is in seconds
        last: TIMESTAMP_S

        @pydantic.validator("last", allow_reuse=True)
        def check_year_from_timestamp(cls, v):
            y = date.fromtimestamp(v).year
            if not y > 2009 and y < 2050:
                err_msg = f"Year {y} for timestamp {v} not within [2009, 2050]"
                raise ValueError(err_msg)
            return v

    # Entries(<time>, <open>, <high>, <low>, <close>, <vwap>, <volume>, <count>)
    _Candle = typing.Tuple[
        Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, int
    ]

    kwargs = {
        pair: (
            # tuple : timestamp, open, high, low, close, vwap, volume, count
            typing.Tuple[_Candle, ...],
            ...,
        ),
        "__base__": _BaseOhlcResp,
    }

    model = pydantic.create_model("_OhlcResponse", **kwargs)  # type: ignore

    return model


class Response:
    """Response model for endpoint https://api.kraken.com/0/public/OHLC"

    Returns:
    --------
        OHLC Response Model

    Model Fields:
    -------------
        `pair_name` : str
            Array of array entries(time, open, high, low, close, vwap, volume, count)
        last : int
            id to be used as since when polling for new, committed OHLC data)

    Usage:
    ------
        model = Response()
        validated_response = model(JSON_response_content)

    """

    def __call__(self, response: dict):

        pairs = list({k: v for k, v in response.items() if k not in ["last"]}.keys())
        if len(pairs) > 1:
            raise ValueError("More than 1 pair in response keys")
        else:
            pair = pairs[0]
        model = _generate_model(pair)
        # print("\nFields", model.__fields__, "\n")
        return model(**response)


# ------------------------------
# Test with Sample Response
# ------------------------------


if __name__ == "__main__":

    data = {
        "XETHXXBT": [
            [
                1591475580,
                "0.02499",
                "0.02499",
                "0.02499",
                "0.02499",
                "0.00000",
                "0.00000000",
                0,
            ],
            [
                1591475640,
                "0.02500",
                "0.02500",
                "0.02500",
                "0.02500",
                "0.02500",
                "9.12201000",
                5,
            ],
            [
                1591475700,
                "0.02499",
                "0.02499",
                "0.02499",
                "0.02499",
                "0.02499",
                "1.28681415",
                2,
            ],
            [
                1591475760,
                "0.02499",
                "0.02499",
                "0.02499",
                "0.02499",
                "0.02499",
                "0.08800000",
                1,
            ],
        ],
        "last": 1591517580,
    }

    data2 = {
        "XETHXXBT": [
            [
                1591475581,
                "0.02499",
                "0.02499",
                "0.02499",
                "0.02499",
                "0.00000",
                "0.00000000",
                0,
            ],
            [
                1591475641,
                "0.02500",
                "0.02500",
                "0.02500",
                "0.02500",
                "0.02500",
                "9.12201000",
                5,
            ],
            [
                1591475701,
                "0.02499",
                "0.02499",
                "0.02499",
                "0.02499",
                "0.02499",
                "1.28681415",
                2,
            ],
            [
                1591475761,
                "0.02499",
                "0.02499",
                "0.02499",
                "0.02499",
                "0.02499",
                "0.08800000",
                1,
            ],
        ],
        "last": 1591517580,
    }

    expect = Response()
    valid = expect(data)
    print("Validated model", valid, "\n")

    valid2 = expect(data2)
    print("Validated model", valid2, "\n")
