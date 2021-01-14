import typing
from datetime import date
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from definitions import TIMEFRAMES, COUNT, TIMESTAMP_S



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


    _BidAskItem = typing.Tuple[Decimal, Decimal, TIMESTAMP_S]

    class Book(pydantic.BaseModel):

         # tuples of price, volume, time
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
            Which are array of array entries(price, volume, timestamp)
    """

    def __new__(_cls, pair: str):
        model = make_model_orderbook(pair)
        return model
