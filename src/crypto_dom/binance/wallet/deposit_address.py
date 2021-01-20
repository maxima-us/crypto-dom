import typing

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import RECV_WINDOW, ASSET


# ============================================================
# DEPOSIT ADDRES (SUPPORTING NETWORK) 
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#deposit-address-supporting-network-user_data

URL = "https://api.binance.com/sapi/v1/capital/deposit/address"
METHOD = "GET"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------

# {
#     "address": "1HPn8Rx2y6nNSfagQBKy27GB99Vbzg89wv",
#     "coin": "BTC",
#     "tag": "",
#     "url": "https://btc.com/1HPn8Rx2y6nNSfagQBKy27GB99Vbzg89wv"
# }


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint https://api.binance.com/sapi/v1/capital/deposit/address

    Model Fields:
    -------------
        coin : str 
        network : str
            If not sent, return default network of the coin (optional)
            You can get network and isDefault in networkList in the response of "GET /sapi/v1/capital/config/getall" (HMAC SHA256).
        timestamp : float
        recvWindow : int
           Number of milliseconds after timestamp the request is valid for (optional)
           Default = 5000
       
    """

    coin: ASSET 
    network: typing.Optional[str]
    timestamp: TIMESTAMP_MS     #FIXME what is this ?
    recvWindow: typing.Optional[RECV_WINDOW]


# ------------------------------
# Response Model
# ------------------------------


class _DepositAddressResp(pydantic.BaseModel):
    
   address: str
   coin: ASSET 
   tag: typing.Optional[str]
   url: pydantic.AnyHttpUrl 


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint https://api.binance.com/sapi/v1/capital/deposit/address

    Type: pydantic.BaseModel or array of pydantic Models
    
    Model Fields:
    -------------
    """

    def __new__(_cls):
        return _DepositAddressResp

        




if __name__ == "__main__":

    data = {
        "address": "1HPn8Rx2y6nNSfagQBKy27GB99Vbzg89wv",
        "coin": "BTC",
        "tag": "",
        "url": "https://btc.com/1HPn8Rx2y6nNSfagQBKy27GB99Vbzg89wv"
    }

    expect = Response()
    valid = expect(**data)
    print("Validated model", valid, "\n")