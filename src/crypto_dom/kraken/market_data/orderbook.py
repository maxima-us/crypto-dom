import typing
from datetime import date
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import COUNT, TIMESTAMP_S
from crypto_dom.kraken.definitions import PAIR


# ============================================================
# ORDERBOOK
# ============================================================


# doc: https://www.kraken.com/features/api#get-order-book

URL = "https://api.kraken.com/0/public/Depth"
METHOD = "GET"


# ------------------------------
# Sample Response (ccxt)
# ------------------------------

#     {
#         "error":[],
#         "result":{
#             "XETHXXBT":{
#                 "asks":[
#                     ["0.023480","4.000",1586321307],
#                     ["0.023490","50.095",1586321306],
#                     ["0.023500","28.535",1586321302],
#                 ],
#                 "bids":[
#                     ["0.023470","59.580",1586321307],
#                     ["0.023460","20.000",1586321301],
#                     ["0.023440","67.832",1586321306],
#                 ]
#             }
#         }
#     }
#


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/public/Depth

    Model Fields:
    -------
        pair : str
            Asset pair to get OHLC data for
        count : int
            maximum number of asks/bids (optional)
    """

    pair: PAIR
    count: typing.Optional[COUNT]


# ------------------------------
# Response Model
# ------------------------------


def _generate_model(pair: str) -> typing.Type[pydantic.BaseModel]:
    "dynamically create the model. Returns a new pydantic model class"

    _BidAskItem = typing.Tuple[Decimal, Decimal, TIMESTAMP_S]

    class _Book(pydantic.BaseModel):

        # tuples of price, volume, time
        asks: typing.Tuple[_BidAskItem, ...]
        bids: typing.Tuple[_BidAskItem, ...]

    kwargs = {pair: (_Book, ...), "__base__": pydantic.BaseModel}

    model = pydantic.create_model("_OrderBookResponse", **kwargs)  # type: ignore

    return model


class Response:
    """Response Model for endpoint https://api.kraken.com/0/public/Depth

    Returns:
    --------
        OrderBook Response Model

    Model Fields:
    -------------
        `pair_name` : str
            Dict of `asks` and `bids`
            Which are array of array entries(price, volume, timestamp)

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
        "XETHXXBT": {
            "asks": [
                ["0.023480", "4.000", 1586321307],
                ["0.023490", "50.095", 1586321306],
                ["0.023500", "28.535", 1586321302],
            ],
            "bids": [
                ["0.023470", "59.580", 1586321307],
                ["0.023460", "20.000", 1586321301],
                ["0.023440", "67.832", 1586321306],
            ],
        }
    }

    expected = Response()
    valid = expected(data)
    print("Validated model", valid, "\n")
