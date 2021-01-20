from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.binance.definitions import SYMBOL


# ============================================================
# AVERAGE PRICe
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#current-average-price

URL = "https://api.binance.com/api/v3/avgPrice"
METHOD = "GET"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


# {
#   "mins": 5,
#   "price": "9.35751834"
# }


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint https://api.binance.com/api/v3/avgPrice

    Model Fields:
    -------------
        symbol : str 
            Asset pair to get price ticker data for
    """

    symbol: SYMBOL 


# ------------------------------
# Response Model
# ------------------------------


class _AveragePriceResp(pydantic.BaseModel):

    mins: int
    price: Decimal 


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint https://api.binance.com/api/v3/avgPrice

    Type: pydantic.BaseModels
    
    Model Fields:
    -------------
        mins : int
        price : Decimal
    """

    def __new__(_cls):
        return _AveragePriceResp