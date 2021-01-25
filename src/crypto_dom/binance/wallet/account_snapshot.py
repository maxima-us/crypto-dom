import typing
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import RECV_WINDOW, ASSET


# ============================================================
# DAILY ACCOUNT SNAPSHOT 
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#daily-account-snapshot-user_data

URL = "https://api.binance.com/sapi/v1/accountSnapshot"
METHOD = "GET"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


# for SPOT

# {
#    "code":200, // 200 for success; others are error codes
#    "msg":"", // error message
#    "snapshotVos":[
#       {
#          "data":{
#             "balances":[
#                {
#                   "asset":"BTC",
#                   "free":"0.09905021",
#                   "locked":"0.00000000"
#                },
#                {
#                   "asset":"USDT",
#                   "free":"1.89109409",
#                   "locked":"0.00000000"
#                }
#             ],
#             "totalAssetOfBtc":"0.09942700"
#          },
#          "type":"spot",
#          "updateTime":1576281599000
#       }
#    ]
# }

# OR
# for MARGIN

# {
#    "code":200, // 200 for success; others are error codes
#    "msg":"", // error message
#    "snapshotVos":[
#       {
#          "data":{
#             "marginLevel":"2748.02909813",
#             "totalAssetOfBtc":"0.00274803",
#             "totalLiabilityOfBtc":"0.00000100",
#             "totalNetAssetOfBtc":"0.00274750",
#             "userAssets":[
#                {
#                   "asset":"XRP",
#                   "borrowed":"0.00000000",
#                   "free":"1.00000000",
#                   "interest":"0.00000000",
#                   "locked":"0.00000000",
#                   "netAsset":"1.00000000"
#                }
#             ]
#          },
#          "type":"margin",
#          "updateTime":1576281599000
#       }
#    ]
# }

# OR
# FOR FUTURES

# {
#    "code":200, // 200 for success; others are error codes
#    "msg":"", // error message
#    "snapshotVos":[
#       {
#          "data":{
#             "assets":[
#                {
#                   "asset":"USDT",
#                   "marginBalance":"118.99782335",
#                   "walletBalance":"120.23811389"
#                }
#             ],
#             "position":[
#                {
#                   "entryPrice":"7130.41000000",
#                   "markPrice":"7257.66239673",
#                   "positionAmt":"0.01000000",
#                   "symbol":"BTCUSDT",
#                   "unRealizedProfit":"1.24029054"
#                }
#             ]
#          },
#          "type":"futures",
#          "updateTime":1576281599000
#       }
#    ]
# }



# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint https://api.binance.com/sapi/v1/accountSnapshot

    Model Fields:
    -------------
        type : str 
            One of SPOT, MARGIN, FUTURES
        timestamp : float
            Timestamp in milliseconds
        startTime : float
            Timestamp in milliseconds (optional)
        endTime : float
            Timestamp in milliseconds (optional)
        limit : int
            Min 5, Max 30, Default 5 (optional)
        recvWindow : int
           Number of milliseconds after timestamp the request is valid for (optional)
           Default = 5000
       
    """

    type: Literal["SPOT", "MARKET", "FUTURES"]
    timestamp: TIMESTAMP_MS     #FIXME what is this ?
    startTime: typing.Optional[TIMESTAMP_MS]
    endTime: typing.Optional[TIMESTAMP_MS]
    limit: typing.Optional[pydantic.conint(ge=5, le=30)]
    recvWindow: typing.Optional[RECV_WINDOW]


# ------------------------------
# Response Model
# ------------------------------


class _SpotData(pydantic.BaseModel):

    class _Balance(pydantic.BaseModel):
        asset: str  #! ASSET missing TWT
        free: Decimal
        locked: Decimal

    balances: typing.Tuple[_Balance, ...]
    totalAssetOfBtc: Decimal


class _MarginData(pydantic.BaseModel):

    class _UserAsset(pydantic.BaseModel):
        asset: str  #! ASSET missing TWT
        borrowed: Decimal
        free: Decimal
        interest: Decimal
        locked: Decimal
        netAsset: Decimal

    marginLevel: typing.Optional[Decimal]
    totalAssetOfBtc : typing.Optional[Decimal]
    totalLiabilityOfBtc: typing.Optional[Decimal]
    totalNetAssetOfBtc: typing.Optional[Decimal]
    userAssets: typing.Tuple[_UserAsset, ...]


class _FuturesData(pydantic.BaseModel):

    class _Asset(pydantic.BaseModel):
        asset: ASSET
        marginBalance: Decimal
        walletBalance: Decimal

    class _Position(pydantic.BaseModel):
        entryPrice: Decimal 
        markPrice: Decimal
        positionAmt: Decimal
        symbol: Decimal
        unRealizedProfit: Decimal

    assets: typing.Tuple[_Asset, ...]
    position: typing.Tuple[_Position, ...]


class _AccountData(pydantic.BaseModel):
    data: typing.Union[_SpotData, _MarginData, _FuturesData]    # FIXME or should we generate model dynamically according to type (arg to be input by user)
    type: Literal["spot", "margin", "futures"]
    updateTime: TIMESTAMP_MS


class _AccountSnapshotResp(pydantic.BaseModel):
    
    code: int   # TODO http code type
    msg: typing.Optional[str]
    snapshotVos : typing.Tuple[_AccountData, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint https://api.binance.com/sapi/v1/accountSnapshot

    Type: pydantic.BaseModel or array of pydantic Models
    
    Model Fields:
    -------------
    """

    def __new__(_cls):
        return _AccountSnapshotResp

        




if __name__ == "__main__":

    data = {
    "code":200,
    "msg":"",
    "snapshotVos":[
      {
        "data":{
            "balances":[
               {
                  "asset":"BTC",
                  "free":"0.09905021",
                  "locked":"0.00000000"
               },
               {
                  "asset":"USDT",
                  "free":"1.89109409",
                  "locked":"0.00000000"
               }
            ],
            "totalAssetOfBtc":"0.09942700"
         },
         "type":"spot",
         "updateTime":1576281599000
      }
   ]
}

    expect = Response()
    valid = expect(**data)
    print("Validated model", valid, "\n")


    data2 = {
   "code":200,
   "msg":"",
   "snapshotVos":[
      {
         "data":{
            "marginLevel":"2748.02909813",
            "totalAssetOfBtc":"0.00274803",
            "totalLiabilityOfBtc":"0.00000100",
            "totalNetAssetOfBtc":"0.00274750",
            "userAssets":[
               {
                  "asset":"XRP",
                  "borrowed":"0.00000000",
                  "free":"1.00000000",
                  "interest":"0.00000000",
                  "locked":"0.00000000",
                  "netAsset":"1.00000000"
               }
            ]
         },
         "type":"margin",
         "updateTime":1576281599000
      }
   ]
}
    
    expect = Response()
    valid = expect(**data2)
    print("Validated model", valid, "\n")



  