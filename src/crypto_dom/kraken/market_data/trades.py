import typing
from datetime import date
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_NS
from crypto_dom.kraken.definitions import PAIR


# ============================================================
# TRADES
# ============================================================


# doc: https://www.kraken.com/features/api#get-recent-trades

URL = "https://api.kraken.com/0/public/Trades"
METHOD = "GET"


# ------------------------------
# Sample Response (ccxt)
# ------------------------------


#     {
#         "error": [],
#         "result": {
#             "XETHXXBT": [
#                 ["0.032310","4.28169434",1541390792.763,"s","l",""]
#             ],
#             "last": "1541439421200678657"
#         }
#     }


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/public/Trades

    Model Fields:
    -------
        pair : str
            Asset pair to get OHLC data for
        since : int
            Return trade data since given id (optional)
            Timestamp in nanoseconds
    """

    pair: PAIR
    since: typing.Optional[TIMESTAMP_NS]

    @pydantic.validator("since", allow_reuse=True)
    def check_year_from_timestamp(cls, v):
        if v == 0 or v is None:
            return v

        # convert from ns to s
        v_s = v * 10 ** -9

        y = date.fromtimestamp(v_s).year
        if not y > 2009 and y < 2050:
            err_msg = f"Year {y} for timestamp {v} not within [2009, 2050]"
            raise ValueError(err_msg)
        return v


# ------------------------------
# Response Model
# ------------------------------


def _generate_model(pair: str) -> typing.Type[pydantic.BaseModel]:
    "dynamically create the model. Returns a new pydantic model class"

    class _BaseTradesResp(pydantic.BaseModel):

        # timestamp received from kraken in ns
        last: TIMESTAMP_NS

        @pydantic.validator("last", allow_reuse=True)
        def check_year_from_timestamp(cls, v, values):
            v_s = v * 10 ** -9

            y = date.fromtimestamp(v_s).year
            if not y > 2009 and y < 2050:
                err_msg = f"Year {y} for timestamp {v} not within [2009, 2050] - check if timestamp is in ns"
                raise ValueError(err_msg)
            return v

    _Trade = typing.Tuple[
        Decimal, Decimal, Decimal, Literal["b", "s"], Literal["m", "l"], typing.Any
    ]

    kwargs = {pair: (typing.Tuple[_Trade, ...], ...), "__base__": _BaseTradesResp}

    model = pydantic.create_model("_TradesResponse", **kwargs)  # type: ignore

    return model


class Response:
    """Response Model for endpoint https://api.kraken.com/0/public/Trades

    Returns:
    --------
        Trades Response Model

    Model Fields:
    -------------
        `pair_name` : str
            Array of array entries(price, volume, time, buy/sell, market/limit, miscellaneous)
        last: int
            Id to be used as since when polling for new trade data

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
        "XETHXXBT": [["0.032310", "4.28169434", 1541390792.763, "s", "l", ""]],
        "last": "1541439421200678657",
    }

    expected = Response()
    valid = expected(data)
    print("Validated model", valid, "\n")
