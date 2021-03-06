import typing
from datetime import date
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_S
from crypto_dom.kraken.definitions import PAIR


# ============================================================
# SPREAD
# ============================================================


# doc: https://www.kraken.com/features/api#get-recent-spread-data

URL = "https://api.kraken.com/0/public/Spread"
METHOD = "GET"


# ------------------------------
# Sample Response
# ------------------------------


# {
#     "error":[],
#     "result":{
#         "XXBTZUSD":[
#             [1610997022,"35803.90000","35804.10000"],
#             [1610997022,"35803.20000","35804.10000"],
#             [1610997022,"35803.30000","35804.10000"]],
#         "last":1610997148}
# }


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/public/Spread

    Model Fields:
    -------
        pair : str
            Asset pair to get spread data for
        since : int
            Timestamp in seconds
            Return trade data since given id (optional)
    """

    pair: PAIR
    since: typing.Optional[TIMESTAMP_S]

    @pydantic.validator("since", allow_reuse=True)
    def check_year_from_timestamp(cls, v):
        if v == 0 or v is None:
            return v

        y = date.fromtimestamp(v).year
        if not y > 2009 and y < 2050:
            err_msg = f"Year {y} for timestamp {v} not within [2009, 2050]"
            raise ValueError(err_msg)
        return v


# ------------------------------
# Response Model
# ------------------------------


def _generate_model(pair: str) -> typing.Type[pydantic.BaseModel]:
    "dynamically create the model. Returns a new pydantic model class"

    class _BaseSpreadResp(pydantic.BaseModel):

        # timestamp received from kraken in s
        last: TIMESTAMP_S

        @pydantic.validator("last", allow_reuse=True)
        def check_year_from_timestamp(cls, v, values):
            # convert from ns to s

            y = date.fromtimestamp(v).year
            if not y > 2009 and y < 2050:
                err_msg = f"Year {y} for timestamp {v} not within [2009, 2050]"
                raise ValueError(err_msg)
            return v

    _Spread = typing.Tuple[Decimal, Decimal, Decimal]

    kwargs = {pair: (typing.Tuple[_Spread, ...], ...), "__base__": _BaseSpreadResp}

    model = pydantic.create_model("_SpreadResponse", **kwargs)  # type: ignore

    return model


class Response:
    """Response Model for endpoint https://api.kraken.com/0/public/Spread

    Returns:
    --------
        Spread Response Model

    Model Fields:
    -------------
        `pair_name` : str
            Array of array entries (time, bid, ask)
        last: int
            Timestamp in seconds
            Id to be used as since when polling for new spread data

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
        "XXBTZUSD": [
            [1610997022, "35803.90000", "35804.10000"],
            [1610997022, "35803.20000", "35804.10000"],
            [1610997022, "35803.30000", "35804.10000"],
        ],
        "last": 1610997148,
    }

    expected = Response()
    valid = expected(data)
    print("Validated model", valid, "\n")
