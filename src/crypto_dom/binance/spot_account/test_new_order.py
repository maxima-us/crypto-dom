import typing
from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_MS
from crypto_dom.binance.definitions import ORDER_RESP_TYPE, ORDER_SIDE, ORDER_TYPE, ORDER_TIF, RECV_WINDOW, SYMBOL


# ============================================================
# TEST NEW ORDER (TRADE)
# ============================================================


# doc: https://binance-docs.github.io/apidocs/spot/en/#test-new-order-trade

URL = "https://api.binance.com/api/v3/order/test"
METHOD = "POST"
WEIGHT = 1


# ------------------------------
# Sample Response (doc)
# ------------------------------


#     {
#     }


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint POST https://api.binance.com/api/v3/order/test

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


        if v in ["STOP-LOSS", "TAKE-PROFIT"]:
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


        if v in ["STOP-LOSS-LIMIT", "TAKE-PROFIT-LIMIT"]:
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


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint POST https://api.binance.com/api/v3/order/test

    Type: pydantic.BaseModel or array of pydantic Models

    Model Fields:
    -------------

    Returns empty dict

    """

    pass
