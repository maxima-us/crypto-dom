import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import COUNT, TIMESTAMP_S


# ============================================================
# CANCEL ALL ORDERS AFTER 
# ============================================================


# doc: https://www.kraken.com/features/api#cancel-all-orders-after

URL = "https://api.kraken.com/0/private/CancelAllOrdersAfter"
METHOD = "POST"


# ------------------------------
# Sample Response
# ------------------------------



# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint POST https://api.kraken.com/0/private/CancelAllOrdersAfter

    Model Fields:
    -------------
        timeout: int
            Timeout specified in seconds. 0 to disable the timer
        nonce : int
            Always increasing unsigned 64 bit integer 
    """

    timeout: COUNT
    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
# ------------------------------


class _CancelAllAfterResponse(pydantic.BaseModel):
    currentTime: TIMESTAMP_S
    triggerTime: TIMESTAMP_S


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint POST https://api.kraken.com/0/private/CancelAllOrdersAfter

    Type: pydantic Model

    Model Fields:
    -------------
        currentTime: float
            Timestamp (in seconds) reflecting when the request has been handled
        triggerTime: float
            Timestamp (in seconds) reflecting when all open orders will be cancelled, unless the timer is extended or disabled 
    """

    def __call__(self, response: dict):
        return _CancelAllAfterResponse(**response)
        
    