import typing
from datetime import date
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_S



# ============================================================
# SPREAD
# ============================================================


# doc: https://www.kraken.com/features/api#get-trade-balance

URL = "https://api.kraken.com/0/public/TradeBalance"
METHOD = "POST"

# ------------------------------
# Request
# ------------------------------

class _TradeBalanceReq(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/public/TradeBalance

    Fields:
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
    asset: str = "ZUSD"
    nonce: pydantic.PositiveInt


# ------------------------------
# Response
# ------------------------------


def generate_model(pair: str) -> typing.Type[pydantic.BaseModel]:
    "dynamically create the model"


    class _BaseTradeBalanceResp(pydantic.BaseModel):

        # timestamp received from kraken in s
        last: TIMESTAMP_S

        @pydantic.validator('last')
        def check_year_from_timestamp(cls, v, values):
            # convert from ns to s

            y = date.fromtimestamp(v).year
            if not y > 2009 and y < 2050:
                err_msg = f"Year {y} for timestamp {v} not within [2009, 2050]"
                raise ValueError(err_msg)
            return v

    _Spread = typing.Tuple[Decimal, Decimal, Decimal]

    kwargs = {
        pair: (typing.Tuple[_Spread, ...], ...),
        "__base__": _BaseTradeBalanceResp
    }

    model = pydantic.create_model(
        '_TradeBalanceResp',
        **kwargs    #type: ignore
    )

    return model



class _TradeBalance(pydantic.BaseModel):
    """Response Model for endpoint https://api.kraken.com/0/public/TradeBalance

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
            margin level = (equity / initial margin) * 100
   """

    eb: Decimal
    tb: Decimal
    m: Decimal
    n: Decimal
    c: Decimal
    v: Decimal
    e: Decimal
    mf: Decimal
    ml: Decimal


#  this class is just to be consistent with our API
class _TradeBalanceResp:

    def __new__(cls):
        return _TradeBalance