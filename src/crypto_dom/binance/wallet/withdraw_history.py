import typing
from decimal import Decimal
import datetime

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS


# ============================================================
# WITHDRAW HISTORY (SUPPORTING NETWORK) 
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#withdraw-history-supporting-network-user_data

URL = "https://api.binance.com/sapi/v1/capital/withdraw/history"
METHOD = "GET"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------

# [
#     {
#         "address": "0x94df8b352de7f46f64b01d3666bf6e936e44ce60",
#         "amount": "8.91000000",
#         "applyTime": "2019-10-12 11:12:02",
#         "coin": "USDT",
#         "id": "b6ae22b3aa844210a7041aee7589627c",
#         "withdrawOrderId": "WITHDRAWtest123", // will not be returned if there's no withdrawOrderId for this withdraw.
#         "network": "ETH", 
#         "transferType": 0,   // 1 for internal transfer, 0 for external transfer   
#         "status": 6,
#         "txId": "0xb5ef8c13b968a406cc62a93a8bd80f9e9a906ef1b3fcf20a2e48573c17659268"
#     },
#     {
#         "address": "1FZdVHtiBqMrWdjPyRPULCUceZPJ2WLCsB",
#         "amount": "0.00150000",
#         "applyTime": "2019-09-24 12:43:45",
#         "coin": "BTC",
#         "id": "156ec387f49b41df8724fa744fa82719",
#         "network": "BTC",
#         "status": 6,
#         "txId": "60fd9007ebfddc753455f95fafa808c4302c836e4d1eebc5a132c36c1d8ac354"
#     }
# ]


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint https://api.binance.com/sapi/v1/capital/withdraw/history

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


class _Withdrawal(pydantic.BaseModel):
    
    address: str
    amount: Decimal
    applyTime: datetime.datetime
    coin: str   # TODO replace with assets
    id: str
    withdrawOrderId: typing.Optional[str]
    network: str
    transferType: typing.Optional[Literal[0, 1]] # 0 for external transfer, 1 for internal
    status: Literal[0,1,2,3,4,5,6]
    txId: str

class _WithdrawHistoryResp(pydantic.BaseModel):

    #placeholder
    data: typing.Tuple[_Withdrawal, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint https://api.binance.com/sapi/v1/capital/withdraw/history

    Type: pydantic.BaseModel or array of pydantic Models
    
    Model Fields:
    -------------
    """

    def __call__(self, response):
        _model = _WithdrawHistoryResp(data=response)
        return _model.data
        




if __name__ == "__main__":

    data = [
    {
        "address": "0x94df8b352de7f46f64b01d3666bf6e936e44ce60",
        "amount": "8.91000000",
        "applyTime": "2019-10-12 11:12:02",
        "coin": "USDT",
        "id": "b6ae22b3aa844210a7041aee7589627c",
        "withdrawOrderId": "WITHDRAWtest123",
        "network": "ETH", 
        "transferType": 0,
        "status": 6,
        "txId": "0xb5ef8c13b968a406cc62a93a8bd80f9e9a906ef1b3fcf20a2e48573c17659268"
    },
    {
        "address": "1FZdVHtiBqMrWdjPyRPULCUceZPJ2WLCsB",
        "amount": "0.00150000",
        "applyTime": "2019-09-24 12:43:45",
        "coin": "BTC",
        "id": "156ec387f49b41df8724fa744fa82719",
        "network": "BTC",
        "status": 6,
        "txId": "60fd9007ebfddc753455f95fafa808c4302c836e4d1eebc5a132c36c1d8ac354"
    }
]

    expect = Response()
    valid = expect(data)
    print("Validated model", valid, "\n")