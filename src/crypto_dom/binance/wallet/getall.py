import typing
from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import RECV_WINDOW, ASSET


# ============================================================
# ALL COINS INFORMATION
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#all-coins-39-information-user_data 

URL = "https://api.binance.com/sapi/v1/capital/config/getall"
METHOD = "GET"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


# [
#     {
#         "coin": "BTC",
#         "depositAllEnable": true,
#         "free": "0.08074558",
#         "freeze": "0.00000000",
#         "ipoable": "0.00000000",
#         "ipoing": "0.00000000",
#         "isLegalMoney": false,
#         "locked": "0.00000000",
#         "name": "Bitcoin",
#         "networkList": [
#             {
#                 "addressRegex": "^(bnb1)[0-9a-z]{38}$",
#                 "coin": "BTC",
#                 "depositDesc": "Wallet Maintenance, Deposit Suspended", // shown only when "depositEnable" is false.
#                 "depositEnable": false,
#                 "isDefault": false,        
#                 "memoRegex": "^[0-9A-Za-z\\-_]{1,120}$",
#                 "minConfirm": 1,  // min number for balance confirmation
#                 "name": "BEP2",
#                 "network": "BNB",            
#                 "resetAddressStatus": false,
#                 "specialTips": "Both a MEMO and an Address are required to successfully deposit your BEP2-BTCB tokens to Binance.",
#                 "unLockConfirm": 0,  // confirmation number for balance unlock 
#                 "withdrawDesc": "Wallet Maintenance, Withdrawal Suspended", // shown only when "withdrawEnable" is false.
#                 "withdrawEnable": false,
#                 "withdrawFee": "0.00000220",
#                 "withdrawMin": "0.00000440"
#             },
#             {
#                 "addressRegex": "^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^(bc1)[0-9A-Za-z]{39,59}$",
#                 "coin": "BTC",
#                 "depositEnable": true,
#                 "insertTime": 1563532929000,
#                 "isDefault": true,
#                 "memoRegex": "",
#                 "minConfirm": 1, 
#                 "name": "BTC",
#                 "network": "BTC",
#                 "resetAddressStatus": false,
#                 "specialTips": "",
#                 "unLockConfirm": 2,
#                 "updateTime": 1571014804000, 
#                 "withdrawEnable": true,
#                 "withdrawFee": "0.00050000",
#                 "withdrawIntegerMultiple": "0.00000001",
#                 "withdrawMin": "0.00100000"
#             }
#         ],
#         "storage": "0.00000000",
#         "trading": true,
#         "withdrawAllEnable": true,
#         "withdrawing": "0.00000000"
#     }
# ]


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint https://api.binance.com/sapi/v1/capital/config/getall

    Model Fields:
    -------------
        timestamp : float
        recvWindow : int
           Number of milliseconds after timestamp the request is valid for (optional)
           Default = 5000
       
    """

    timestamp: TIMESTAMP_MS     #FIXME what is this ?
    recvWindow: typing.Optional[RECV_WINDOW]


# ------------------------------
# Response Model
# ------------------------------


class _Network (pydantic.BaseModel):

    addressRegex: str
    coin: ASSET
    despositDesc: typing.Optional[str]
    depositEnable: bool
    insertTime: typing.Optional[TIMESTAMP_MS]
    isDefault: bool
    memoRegex: str
    minConfirm: pydantic.PositiveInt
    name: str
    network: str
    resetAddressStatus: bool
    specialTips: str
    unLockConfirm: int
    updateTime: typing.Optional[TIMESTAMP_MS]
    withdrawDesc: typing.Optional[str]
    withdrawEnable: bool
    withdrawFee: Decimal
    withdrawIntegerMultiple: typing.Optional[Decimal]
    withdrawMin: Decimal


class _CoinSpecs(pydantic.BaseModel):

    coin: ASSET
    depositAllEnable: bool
    free: Decimal
    ipoable: Decimal
    ipoing: Decimal
    isLegalMoney: bool
    locked: Decimal
    name: str
    networkList: typing.Tuple[_Network, ...]
    storage: Decimal
    trading: bool
    withdrawAllEnable: bool
    withdrawing: Decimal


class _GetAllResp(pydantic.BaseModel):

    #placeholder
    data: typing.Tuple[_CoinSpecs, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint https://api.binance.com/sapi/v1/capital/config/getall

    Type: pydantic.BaseModel or array of pydantic Models
    
    Model Fields:
    -------------
    """

    def __call__(self, response):
        _model = _GetAllResp(data=response)
        return _model.data







if __name__ == "__main__":

    data = [
    {
        "coin": "BTC",
        "depositAllEnable": True,
        "free": "0.08074558",
        "freeze": "0.00000000",
        "ipoable": "0.00000000",
        "ipoing": "0.00000000",
        "isLegalMoney": False,
        "locked": "0.00000000",
        "name": "Bitcoin",
        "networkList": [
            {
                "addressRegex": "^(bnb1)[0-9a-z]{38}$",
                "coin": "BTC",
                "depositDesc": "Wallet Maintenance, Deposit Suspended",
                "depositEnable": False,
                "isDefault": False,        
                "memoRegex": "^[0-9A-Za-z\\-_]{1,120}$",
                "minConfirm": 1,
                "name": "BEP2",
                "network": "BNB",            
                "resetAddressStatus": False,
                "specialTips": "Both a MEMO and an Address are required to successfully deposit your BEP2-BTCB tokens to Binance.",
                "unLockConfirm": 0,
                "withdrawDesc": "Wallet Maintenance, Withdrawal Suspended",
                "withdrawEnable": False,
                "withdrawFee": "0.00000220",
                "withdrawMin": "0.00000440"
            },
            {
                "addressRegex": "^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^(bc1)[0-9A-Za-z]{39,59}$",
                "coin": "BTC",
                "depositEnable": True,
                "insertTime": 1563532929000,
                "isDefault": True,
                "memoRegex": "",
                "minConfirm": 1, 
                "name": "BTC",
                "network": "BTC",
                "resetAddressStatus": False,
                "specialTips": "",
                "unLockConfirm": 2,
                "updateTime": 1571014804000, 
                "withdrawEnable": True,
                "withdrawFee": "0.00050000",
                "withdrawIntegerMultiple": "0.00000001",
                "withdrawMin": "0.00100000"
            }
        ],
        "storage": "0.00000000",
        "trading": True,
        "withdrawAllEnable": True,
        "withdrawing": "0.00000000"
    }
]

    expect = Response()
    valid = expect(data)
    print("Validated model", valid, "\n")