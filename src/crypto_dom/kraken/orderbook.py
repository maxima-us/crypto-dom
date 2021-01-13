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


# doc: https://www.kraken.com/features/api#get-order-book 

URL = "https://api.kraken.com/0/public/Depth"
METHOD = "GET"

# ------------------------------
# Request
# ------------------------------

class _OrderbookReq(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/public/Depth

    Fields:
    -------
        pair : str 
            Asset pair to get OHLC data for
        count : int 
            maximum number of asks/bids (optional) 
    """

    pair: str
    count: typing.Optional[COUNT]


# ------------------------------
# Response
# ------------------------------


def make_model_orderbook(pair: str) -> typing.Type[pydantic.BaseModel]:
    "dynamically create the model"


    _BidAskItem = typing.Tuple[Decimal, Decimal, Decimal]

    class Book(pydantic.BaseModel):

         # tuples of price, volume, time
        # where timestamps are in s
        asks: typing.Tuple[_BidAskItem, ...]
        bids: typing.Tuple[_BidAskItem, ...]

    
    kwargs = {
        pair: (Book, ...),
        "__base__": pydantic.BaseModel
    }

    model = pydantic.create_model(
        '_OrderBookResp',
        **kwargs    #type: ignore
    )

    return model



class _OrderBookResp:
    """Response Model for endpoint https://api.kraken.com/0/public/Depth

    Fields:
    -------
        `pair_name` : str
            Dict of `asks` and `bids`
            Which are array of array entries(<price>, <volume>, <timestamp>)
    """

    def __new__(_cls, pair: str):
        print("calling new")
        model = make_model_orderbook(pair)
        return model
