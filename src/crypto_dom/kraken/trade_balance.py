import typing
from datetime import date
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_S
from crypto_dom.kraken.definitions import ASSET


# ============================================================
# TRADE BALANCE
# ============================================================


# doc: https://www.kraken.com/features/api#get-trade-balance

URL = "https://api.kraken.com/0/private/TradeBalance"
METHOD = "POST"


# ------------------------------
# Request Model
# ------------------------------


class TradeBalanceReq(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/private/TradeBalance

    Model Fields:
    -------
        aclass : str 
            Asset Class (optional)
                currency (default)
        asset : str 
            Base asset used to determine balance
                (default = ZUSD)
        nonce: int
            Always increasing unsigned 64 bit integer
    """

    aclass: typing.Optional[str]
    asset: ASSET = "ZUSD"
    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
# ------------------------------


class _TradeBalance(pydantic.BaseModel):

    eb: Decimal
    tb: Decimal
    m: Decimal
    n: Decimal
    c: Decimal
    v: Decimal
    e: Decimal
    mf: Decimal
    ml: typing.Optional[Decimal]


#  this class is just to be consistent with our API
class TradeBalanceResp:
    """Response Model for endpoint https://api.kraken.com/0/private/TradeBalance

    Fields:
    -------
        eb : Decimal
            equivalent balance (combined balance of all currencies))
        tb: Decimal
            trade balance (combined balance of all equity currencies)s
        m: Decimal
            margin amount of open positions
        n: Decimal
            unrealized net profit/loss of open positions
        c: Decimal
            cost basis of open positions
        v: Decimal
            current floating valuation of open positions
        e: Decimal
            equity = trade balance + unrealized net profit/loss
        mf: Decimal
            free margin = equity - initial margin (maximum margin available to open new positions)
        ml: Decimal
            margin level = (equity / initial margin) * 100 (optional)
   """

    def __new__(cls):
        return _TradeBalance