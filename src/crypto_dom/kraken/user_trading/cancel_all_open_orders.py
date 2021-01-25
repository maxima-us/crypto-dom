import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import COUNT


# ============================================================
# ADD STANDARD ORDER 
# ============================================================


# doc: https://www.kraken.com/features/api#cancel-all-open-orders 

URL = "https://api.kraken.com/0/private/CancelAll"
METHOD = "POST"


# ------------------------------
# Sample Response
# ------------------------------



# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint POST https://api.kraken.com/0/private/CancelAll

    Model Fields:
    -------------
        nonce : int
            Always increasing unsigned 64 bit integer 
    """

    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
# ------------------------------


class _CancelAllResponse(pydantic.BaseModel):
    count: COUNT 


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint POST https://api.kraken.com/0/private/CancelAll

    Type: pydantic Model

    Model Fields:
    -------------
        count: int
            Number of orders canceled
    """

    def __call__(self, response: dict):
        return _CancelAllResponse(**response)
        
    