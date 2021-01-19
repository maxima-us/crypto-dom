import typing
from decimal import Decimal

import pydantic
import stackprinter
from typing_extensions import Literal
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import ORDER_TYPE, RATE_LIMITE_TYPE, SYMBOL_PERMISSIONS, SYMBOL_STATUS


# ============================================================
# EXCHANGE INFORMATION
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#exchange-information

URL = "https://api.binance.com/api/v3/exchangeInfo"
METHOD = "GET"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


# {
#   "timezone": "UTC",
#   "serverTime": 1565246363776,
#   "rateLimits": [
#     {
#       //These are defined in the `ENUM definitions` section under `Rate Limiters (rateLimitType)`.
#       //All limits are optional
#     }
#   ],
#   "exchangeFilters": [
#     //These are the defined filters in the `Filters` section.
#     //All filters are optional.
#   ],
#   "symbols": [
#     {
#       "symbol": "ETHBTC",
#       "status": "TRADING",
#       "baseAsset": "ETH",
#       "baseAssetPrecision": 8,
#       "quoteAsset": "BTC",
#       "quotePrecision": 8,
#       "quoteAssetPrecision": 8,
#       "orderTypes": [
#         "LIMIT",
#         "LIMIT_MAKER",
#         "MARKET",
#         "STOP_LOSS",
#         "STOP_LOSS_LIMIT",
#         "TAKE_PROFIT",
#         "TAKE_PROFIT_LIMIT"
#       ],
#       "icebergAllowed": true,
#       "ocoAllowed": true,
#       "isSpotTradingAllowed": true,
#       "isMarginTradingAllowed": true,
#       "filters": [
#         //These are defined in the Filters section.
#         //All filters are optional
#       ],
#       "permissions": [
#          "SPOT",
#          "MARGIN"
#       ]
#     }
#   ]
# }


# ------------------------------
# Request Model
# ------------------------------


# No Parameters
class Request(pydantic.BaseModel):
    """Request model for endpoint https://api.binance.com/api/v3/exchangeInfo
    """

    pass
    

# ------------------------------
# Response Model
# ------------------------------


class _SymbolsInfo(pydantic.BaseModel):

    symbol: str
    status: SYMBOL_STATUS
    baseAsset: str
    baseAssetPrecision: pydantic.PositiveInt
    quoteAsset: str
    quoteAssetPrecision: pydantic.PositiveInt
    baseCommissionPrecision: pydantic.PositiveInt
    quoteCommissionPrecision: pydantic.PositiveInt
    orderTypes: typing.List[ORDER_TYPE]
    icebergAllowed: bool
    ocoAllowed: bool
    quoteOrderQtyMarketAllowed: bool
    isSpotTradingAllowed: bool
    isMarginTradingAllowed: bool
    filters: list
    permissions: typing.List[SYMBOL_PERMISSIONS]


class _ExchangeInfoResp(pydantic.BaseModel):

    timezone: Literal["UTC"]
    serverTime: TIMESTAMP_MS
    rateLimits: typing.List[RATE_LIMITE_TYPE]
    exchangeFilters: typing.List[str]   #TODO define filters in definitions
    symbols: typing.Tuple[_SymbolsInfo, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint https://api.binance.com/api/v3/exchangeInfo

    Type: pydantic.BaseModel
    
    Model Fields:
    -------------
        timezone : str
        serverTime : float
            Timestamp in milliseconds
        rateLimiters : List[str]
        exchangeFilters : List[str]
        symbols : dict


    Note:
    -----
    Fields of symbols dict
        symbol : str
        status : str
        baseAsset : str
        baseAssetPrecision : int
        quoteAsset : str
        quoteAssetPrecision : int
        orderTypes : List[str]
        icebergAllowed : bool
        ocoAllowed : bool
        isSpotTradingAllowed : bool
        isMarginTradingAllowed : bool
        filters : List[str]
        permissions : List[str]
    """

    def __new__(_cls):
        return _ExchangeInfoResp
        

