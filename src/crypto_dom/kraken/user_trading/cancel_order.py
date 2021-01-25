import typing

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import COUNT
from crypto_dom.kraken.definitions import ORDERID


# ============================================================
# ADD STANDARD ORDER 
# ============================================================


# doc: https://www.kraken.com/features/api#cancel-open-order 

URL = "https://api.kraken.com/0/private/CancelOrder"
METHOD = "POST"


# ------------------------------
# Sample Response
# ------------------------------



# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint POST https://api.kraken.com/0/private/CancelOrder 

    Model Fields:
    -------------
        txid: str
            Transaction Id
        nonce : int
            Always increasing unsigned 64 bit integer 
    """

    txid: ORDERID 
    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
# ------------------------------


class _CancelOrderResponse(pydantic.BaseModel):
    count: COUNT 
    pending: typing.Tuple[ORDERID, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint POST https://api.kraken.com/0/private/CancelOrder 

    Type: pydantic Model
    
    Model Fields:
    -------------
        count: int
            Number of orders canceled
        pending: List[str]
            if set, orders that are pending cancellation
    """

    def __call__(self, response: dict):
        return _CancelOrderResponse(**response)
        
    