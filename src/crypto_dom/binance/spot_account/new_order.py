import typing
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import ORDER_RESP_TYPE, ORDER_SIDE, ORDER_STATUS, ORDER_TYPE, ORDER_TIF, RECV_WINDOW, SYMBOL, ASSET


# ============================================================
# NEW ORDER (TRADE)
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#new-order-trade

URL = "https://api.binance.com/api/v3/order"
METHOD = "POST"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


# RESPONSE ACK

# {
#   "symbol": "BTCUSDT",
#   "orderId": 28,
#   "orderListId": -1, //Unless OCO, value will be -1
#   "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
#   "transactTime": 1507725176595
# }


# RESPONSE RESULT

# {
#   "symbol": "BTCUSDT",
#   "orderId": 28,
#   "orderListId": -1, //Unless OCO, value will be -1
#   "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
#   "transactTime": 1507725176595,
#   "price": "0.00000000",
#   "origQty": "10.00000000",
#   "executedQty": "10.00000000",
#   "cummulativeQuoteQty": "10.00000000",
#   "status": "FILLED",
#   "timeInForce": "GTC",
#   "type": "MARKET",
#   "side": "SELL"
# }


# RESPONSE FULL

# {
#   "symbol": "BTCUSDT",
#   "orderId": 28,
#   "orderListId": -1, //Unless OCO, value will be -1
#   "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
#   "transactTime": 1507725176595,
#   "price": "0.00000000",
#   "origQty": "10.00000000",
#   "executedQty": "10.00000000",
#   "cummulativeQuoteQty": "10.00000000",
#   "status": "FILLED",
#   "timeInForce": "GTC",
#   "type": "MARKET",
#   "side": "SELL",
#   "fills": [
#     {
#       "price": "4000.00000000",
#       "qty": "1.00000000",
#       "commission": "4.00000000",
#       "commissionAsset": "USDT"
#     },
#     {
#       "price": "3999.00000000",
#       "qty": "5.00000000",
#       "commission": "19.99500000",
#       "commissionAsset": "USDT"
#     },
#     {
#       "price": "3998.00000000",
#       "qty": "2.00000000",
#       "commission": "7.99600000",
#       "commissionAsset": "USDT"
#     },
#     {
#       "price": "3997.00000000",
#       "qty": "1.00000000",
#       "commission": "3.99700000",
#       "commissionAsset": "USDT"
#     },
#     {
#       "price": "3995.00000000",
#       "qty": "1.00000000",
#       "commission": "3.99500000",
#       "commissionAsset": "USDT"
#     }
#   ]
# }


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint POST https://api.binance.com/api/v3/order

    Model Fields:
    -------------

        symbol : str
        side : str enum
            [BUY, SELL]
        type : str enum
            [MARKET, LIMIT, STOP_LOSS, TAKE_PROFIT, STOP_LOSS_LIMIT, TAKE_PROFIT_LIMIT, LIMIT_MAKER]
        timeInForce : enum string
            [GTC, IOC, FOK] (optionalm)
        quantity : Decimal
            (optional)
        quoteOrderQty : Decimal
            (optional)
        price : Decimal
            (optional)
        newClientOrderId : str
            (optional)
        stopPrice : Decimal
            (optional)
        icebergQty : Decimal
            (optional)
        newOrderRespType : str enum
            [ACK, RESULT, FULL] (optional)

        timestamp : float
        recvWindow : int
           Number of milliseconds after timestamp the request is valid for (optional)
           Default = 5000

    """

    symbol: SYMBOL
    side: ORDER_SIDE
    timeInForce: typing.Optional[ORDER_TIF]
    quantity: typing.Optional[Decimal]
    quoteOrderQty: typing.Optional[Decimal]
    price: typing.Optional[Decimal]
    newClientOrderId: typing.Optional[str]
    stopPrice: typing.Optional[Decimal]
    icebergQty: typing.Optional[Decimal]
    newOrderRespType: typing.Optional[ORDER_RESP_TYPE]

    timestamp: TIMESTAMP_MS
    recvWindow: typing.Optional[RECV_WINDOW]

    # needs to be last param because of validation (pydantic validates each field in order it was declared)
    type: ORDER_TYPE


    @pydantic.validator("type")
    def _check_mandatory_args(cls, v, values):

        missing_fields = []
        unexpected_fields = []

        qty = values.get("quantity", None)
        quoteOrderQty = values.get("quoteOrderQty", None)
        tif = values.get("timeInForce", None)
        price = values.get("price", None)
        stop = values.get("stopPrice", None)


        if v == "MARKET":
            # one of orderQty or quoteOrderQty
            if (qty is None and quoteOrderQty is None) or (qty and quoteOrderQty):
                raise ValueError(f"Must set one of [orderQty, quoteOrderQty] - Given: {qty} {quoteOrderQty}")

            # no additional params
            if tif:
                unexpected_fields.append("timeInForce")
            if price:
                unexpected_fields.append("price")


        if v == "LIMIT":
            # check mandatory params
            if tif is None:
                missing_fields.append("timeInForce")
            if price is None:
                missing_fields.append("price")
            if qty is None:
                missing_fields.append("quantity")

            #no additional params
            if stop:
                unexpected_fields.append("stopPrice")
            if quoteOrderQty:
                unexpected_fields.append("quoteOrderQty")


        if v in ["STOP_LOSS", "TAKE_PROFIT"]:
            # mandatory params
            if qty is None:
                missing_fields.append("quantity")
            if stop is None:
                missing_fields.append("stopPrice")

            #no additional params
            if price:
                unexpected_fields.append("price")
            if quoteOrderQty:
                unexpected_fields.append("quoteOrderQty")
            if tif:
                unexpected_fields.append("timeInForce")


        if v in ["STOP_LOSS_LIMIT", "TAKE_PROFIT_LIMIT"]:
            # mandatory params
            if qty is None:
                missing_fields.append("quantity")
            if stop is None:
                missing_fields.append("stopPrice")
            if tif is None:
                missing_fields.append("timeInForce")
            if price is None:
                missing_fields.append("price")

            #no additional params
            if quoteOrderQty:
                unexpected_fields.append("quoteOrderQty")


        if any(missing_fields, unexpected_fields):
            raise ValueError("Missing fields :", *missing_fields, "\n", "Unexpected fields :", *unexpected_fields)


        return v



# ------------------------------
# Response Model
# ------------------------------


class _Fill(pydantic.BaseModel):
    price: Decimal
    qty: Decimal
    commission: Decimal
    commissionAsset: ASSET


class _NewOrderResponseACK(pydantic.BaseModel):
    symbol: SYMBOL
    orderId: pydantic.PositiveInt
    orderListId: pydantic.conint(ge=-1)
    clientOrderId: typing.Optional[str]
    transactTime: TIMESTAMP_MS


class _NewOrderResponseRESULT(_NewOrderResponseACK):
    price: Decimal
    origQty: Decimal
    executedQty: Decimal
    cummulativeQuoteQty: Decimal
    status: ORDER_STATUS
    timeInForce: ORDER_TIF
    type: ORDER_TYPE
    side: ORDER_SIDE


class _NewOrderResponseFULL(_NewOrderResponseRESULT):
    fills: typing.Tuple[_Fill, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint POST https://api.binance.com/api/v3/order

    Type: array of pydantic Models

    Args:
    -----
        newOrderRespType: str enum
            [ACK, RESULT, FULL]

    Model Fields:
    -------------
        Conditional

    """

    def __new__(_cls, newOrderRespType: Literal["ACK", "RESULT", "FULL"]):
        
        if newOrderRespType == "ACK":
            return _NewOrderResponseACK
        elif newOrderRespType == "RESULT":
            return _NewOrderResponseRESULT
        elif newOrderRespType == "FULL":
            return _NewOrderResponseFULL
        else:
            raise TypeError
    



if __name__ == "__main__":
    dataACK = {
  "symbol": "BTCUSDT",
  "orderId": 28,
  "orderListId": -1,
  "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
  "transactTime": 1507725176595
}

    model = Response("ACK")
    model(**dataACK)


    dataRES = {
  "symbol": "BTCUSDT",
  "orderId": 28,
  "orderListId": -1,
  "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
  "transactTime": 1507725176595,
  "price": "0.00000000",
  "origQty": "10.00000000",
  "executedQty": "10.00000000",
  "cummulativeQuoteQty": "10.00000000",
  "status": "FILLED",
  "timeInForce": "GTC",
  "type": "MARKET",
  "side": "SELL"
}

    model = Response("RESULT")
    model(**dataRES)


    dataFULL = {
  "symbol": "BTCUSDT",
  "orderId": 28,
  "orderListId": -1,
  "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
  "transactTime": 1507725176595,
  "price": "0.00000000",
  "origQty": "10.00000000",
  "executedQty": "10.00000000",
  "cummulativeQuoteQty": "10.00000000",
  "status": "FILLED",
  "timeInForce": "GTC",
  "type": "MARKET",
  "side": "SELL",
  "fills": [
    {
      "price": "4000.00000000",
      "qty": "1.00000000",
      "commission": "4.00000000",
      "commissionAsset": "USDT"
    },
    {
      "price": "3999.00000000",
      "qty": "5.00000000",
      "commission": "19.99500000",
      "commissionAsset": "USDT"
    },
    {
      "price": "3998.00000000",
      "qty": "2.00000000",
      "commission": "7.99600000",
      "commissionAsset": "USDT"
    },
    {
      "price": "3997.00000000",
      "qty": "1.00000000",
      "commission": "3.99700000",
      "commissionAsset": "USDT"
    },
    {
      "price": "3995.00000000",
      "qty": "1.00000000",
      "commission": "3.99500000",
      "commissionAsset": "USDT"
    }
  ]
}

    model = Response("FULL")
    model(**dataFULL)