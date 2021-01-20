import typing
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS


# ============================================================
# DEPOSIT HISTORY (SUPPORTING NETWORK) 
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#deposit-history-supporting-network-user_data

URL = "https://api.binance.com/sapi/v1/capital/deposit/hiscrec"
METHOD = "GET"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


# [
#     {
#         "amount":"0.00999800",
#         "coin":"PAXG",
#         "network":"ETH",
#         "status":1,
#         "address":"0x788cabe9236ce061e5a892e1a59395a81fc8d62c",
#         "addressTag":"",
#         "txId":"0xaad4654a3234aa6118af9b4b335f5ae81c360b2394721c019b5d1e75328b09f3",
#         "insertTime":1599621997000,
#         "transferType":0,
#         "confirmTimes":"12/12"
#     },
#     {
#         "amount":"0.50000000",
#         "coin":"IOTA",
#         "network":"IOTA",
#         "status":1,
#         "address":"SIZ9VLMHWATXKV99LH99CIGFJFUMLEHGWVZVNNZXRJJVWBPHYWPPBOSDORZ9EQSHCZAMPVAPGFYQAUUV9DROOXJLNW",
#         "addressTag":"",
#         "txId":"ESBFVQUTPIWQNJSPXFNHNYHSQNTGKRVKPRABQWTAXCDWOAKDKYWPTVG9BGXNVNKTLEJGESAVXIKIZ9999",
#         "insertTime":1599620082000,
#         "transferType":0,
#         "confirmTimes":"1/1"
#     }
# ]


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint https://api.binance.com/sapi/v1/capital/deposit/hisrec

    Model Fields:
    -------------
        coin : str 
        status : int
            Default 0 (0:Email Sent,1:Cancelled 2:Awaiting Approval 3:Rejected 4:Processing 5:Failure 6:Completed) (optional)
        offset: : int
            default = 0 (optional)
        limit : int
            (optional)
        startTime : float
            Timestamp in milliseconds (optional)
        endTime : float
            Timestamp in milliseconds (optional)
        timestamp : float
        recvWindow : int
           Number of milliseconds after timestamp the request is valid for (optional)
           Default = 5000
       
    """

    coin: str # TODO add asset type
    status: typing.Optional[Literal[0, 1, 2, 3, 4, 5, 6]]
    offset: typing.Optional[int]
    limit: typing.Optional[int]
    startTime: typing.Optional[TIMESTAMP_MS]
    endTime: typing.Optional[TIMESTAMP_MS]

    timestamp: TIMESTAMP_MS     #FIXME what is this ?
    recvWindow: typing.Optional[pydantic.conint(le=60000)] # TODO add to definitions


# ------------------------------
# Response Model
# ------------------------------


class _Deposit(pydantic.BaseModel):
    
    amount: Decimal
    coin: str   # TODO replace with assets
    network: str
    status: Literal[0,1,2,3,4,5,6]
    address: str
    addressTag: str
    txId: str
    insertTime: TIMESTAMP_MS
    transferType: typing.Optional[Literal[0, 1]] # 0 for external transfer, 1 for internal
    confirmTimes: str

class _DepositHistoryResp(pydantic.BaseModel):

    #placeholder
    data: typing.Tuple[_Deposit, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint https://api.binance.com/sapi/v1/capital/deposit/hisrec

    Type: pydantic.BaseModel or array of pydantic Models
    
    Model Fields:
    -------------
    """

    def __call__(self, response):
        _model = _DepositHistoryResp(data=response)
        return _model.data
        




if __name__ == "__main__":

    data = [
    {
        "amount":"0.00999800",
        "coin":"PAXG",
        "network":"ETH",
        "status":1,
        "address":"0x788cabe9236ce061e5a892e1a59395a81fc8d62c",
        "addressTag":"",
        "txId":"0xaad4654a3234aa6118af9b4b335f5ae81c360b2394721c019b5d1e75328b09f3",
        "insertTime":1599621997000,
        "transferType":0,
        "confirmTimes":"12/12"
    },
    {
        "amount":"0.50000000",
        "coin":"IOTA",
        "network":"IOTA",
        "status":1,
        "address":"SIZ9VLMHWATXKV99LH99CIGFJFUMLEHGWVZVNNZXRJJVWBPHYWPPBOSDORZ9EQSHCZAMPVAPGFYQAUUV9DROOXJLNW",
        "addressTag":"",
        "txId":"ESBFVQUTPIWQNJSPXFNHNYHSQNTGKRVKPRABQWTAXCDWOAKDKYWPTVG9BGXNVNKTLEJGESAVXIKIZ9999",
        "insertTime":1599620082000,
        "transferType":0,
        "confirmTimes":"1/1"
    }
]

    expect = Response()
    valid = expect(data)
    print("Validated model", valid, "\n")