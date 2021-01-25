import typing
from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_S
from crypto_dom.kraken.definitions import ORDERTYPE, PAIR, ORDERSIDE, FLAGS, ORDERID, LEVERAGE


# ============================================================
# ADD STANDARD ORDER 
# ============================================================


# doc: https://www.kraken.com/features/api#add-standard-order

URL = "https://api.kraken.com/0/private/AddOrder"
METHOD = "POST"


# ------------------------------
# Sample Response
# ------------------------------



# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request model for endpoint POST https://api.kraken.com/0/private/AddOrder 

    Model Fields:
    -------------
        pair : str
        type : str enum
            [buy, sell]
        ordertype : str enum
            [market, limit, stop-loss, take-profit, stop-loss-limit, take-profit-limit, settle-position]
        price : Decimal
            Dependent upon ordertype (optional)
        price2 : Decimal
            Dependent upon ordertype (optional)
        volume : Decimal
            Order volume in lots
        leverage : int
            Default = None (optional)
        oflags : List[str enum]
            comma delimited list of order flags (optional)
            [fcib, fciq, nompp, post]
        starttm : float
            Timestamp in seconds (optional)
            0 = now (default)
            +<n> = schedule start time <n> seconds from now
            <n> = unix timestamp of start time
        expiretm : float 
            Timestamp in seconds (optional)
            0 = now (default)
            +<n> = expire <n> seconds from now
            <n> = unix timestamp of start time
        userref : int
            user reference id - 32-bit signed number (optional)
        validate : bool
            Validate inputs only - Do not submit order (optional)
        nonce : int
            Always increasing unsigned 64 bit integer 

    Note:
    -----
        optional closing order to add to system when order gets filled:
            close[ordertype] = order type
            close[price] = price
            close[price2] = secondary price

        Prices can be preceded by +, -, or # to signify the price as a relative amount 
        (with the exception of trailing stops, which are always relative). 
            + adds the amount to the current offered price. 
            - subtracts the amount from the current offered price. 
            # will either add or subtract the amount to the current offered price, 
              depending on the type and order type used.

        Relative prices can be suffixed with a % to signify the relative amount as a percentage of the offered price.

        For orders using leverage, 0 can be used for the volume to auto-fill the volume needed to close out your position.

    """

    symbol: PAIR 
    type: ORDERSIDE
    price: typing.Optional[Decimal]
    price2: typing.Optional[Decimal]
    volume: Decimal
    leverage: typing.Optional[LEVERAGE] # TODO add definition
    oflags: typing.Optional[FLAGS]
    starttm: typing.Optional[TIMESTAMP_S]
    expiretm: typing.Optional[TIMESTAMP_S]
    userref: typing.Optional[pydantic.PositiveInt]
    validate: typing.Optional[bool]

    nonce: pydantic.PositiveInt

    # needs to be last param because of validation (pydantic validates each field in order it was declared)
    ordertype: ORDERTYPE


    @pydantic.validator("ordertype")
    def _check_mandatory_args(cls, v, values):

        missing_fields = []
        unexpected_fields = []

        price = values.get("price", None)
        price2 = values.get("price2", None)

        if v == "market":
            if price:
                unexpected_fields.append("price")
            if price2:
                unexpected_fields.append("price2")

        if v in ["limit", "stop-loss", "take-profit"]:
            if not price:
                missing_fields.append("price")
            if price2:
                unexpected_fields.append("price2")

        if v in ["stop-loss-limit", "take-profit-limit"]:
            if not price:
                missing_fields.append("price")
            if not price2:
                missing_fields.append("price2")

        if any(missing_fields, unexpected_fields):
            raise ValueError("Missing fields :", *missing_fields, "\n", "Unexpected fields :", *unexpected_fields)

        return v


# ------------------------------
# Response Model
# ------------------------------


class _OrderDescr(pydantic.BaseModel):
    order: str
    close: typing.Optional[str]


class _AddOrderResponse(pydantic.BaseModel):
    descr: _OrderDescr
    txid: typing.Tuple[ORDERID, ...]


#  this class is just to be consistent with our API
class Response:
    """Validated Response for endpoint POST https://api.kraken.com/0/private/AddOrder 

    Type: pydantic Model


    Model Fields:
    -------------
        descr : dict
            Order Description Info
        txid : List[str]
            Array of transaction ids for order
            (if order was added successfully)

    Note:
    -----
        Order Description Info keys:
            order: str
                Order description
            close: 
                Conditional close order description (if conditional close set)
    """

    def __call__(self, response: dict):
        return _AddOrderResponse(**response)
        
    