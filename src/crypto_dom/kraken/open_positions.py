import typing
from datetime import date
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.definitions import TIMESTAMP_S
from crypto_dom.kraken.definitions import (
    ORDERID,
    ORDERTYPE,
    ORDERSIDE,
    FLAGS
)


# ============================================================
# OPEN POSITIONS
# ============================================================


# doc: https://www.kraken.com/features/api#get-open-positions

URL = "https://api.kraken.com/0/private/OpenPositions"
METHOD = "POST"


# ------------------------------
# Request Model
# ------------------------------


class OpenPositionsReq(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/private/OpenPositions

    Model Fields:
    -------
        txid : List[str]
            Comma delimited list of transaction ids to restrict output to 
        docalcs: bool
            Whether or not to include profit/loss calculations (optional)
                default = false
        consolidation: Literal[market]
             what to consolidate the positions data around (optional)
                market = will consolidate positions based on market pair
        nonce: int
            Always increasing unsigned 64 bit integer
    """

    txid: typing.List[ORDERID]
    docalcs: typing.Optional[bool]
    consolidation: typing.Optional[Literal["market"]]
    nonce: pydantic.PositiveInt


# ------------------------------
# Response Model
# ------------------------------


def _generate_model(keys: typing.List[ORDERID]) -> typing.Type[pydantic.BaseModel]:
    "dynamically create the model"


    class _Position(pydantic.BaseModel):

        ordertxid: ORDERID
        pair: str
        time: TIMESTAMP_S
        type: ORDERSIDE
        ordertype: ORDERTYPE
        cost: Decimal
        fee: Decimal
        vol: Decimal
        vol_closed: Decimal
        margin: Decimal
        value: typing.Optional[Decimal]
        net: typing.Optional[Decimal]
        misc: typing.List[typing.Any]
        oflags: FLAGS

        #FIXME! not in kraken doc
        terms: str
        rollovertm: Decimal

       

    # we do not know the keys in advance, only the type of their value
    kwargs = {
        **{k: (_Position, ...) for k in keys},
        "__base__": pydantic.BaseModel
    }

    model = pydantic.create_model(
        '_OpenPositionsResp',
        **kwargs    #type: ignore
    )

    return model


class OpenPositionsResp(pydantic.BaseModel):
    """Response Model for endpoint https://api.kraken.com/0/private/OpenPositions

    Model Fields:
    -------
        `Position TxId`: open position info
            mapping of position txid to their info
                position txid : str
                position info : dict
    
    Note:
    -----
        Order Info dict type:
            ordertxid: str
                order responsible for execution of trade
            pair: str
                asset pair
            time: float
                unix timestamp of trade (in seconds)
            type: Literal["buy", "sell"]
                type of order used to open position
            ordertype: Literal["market", "limit"]
                order type used to open position
            cost: Decimal
                opening cost of position (quote currency unless viqc set in oflags)
            fee: Decimal
                opening fee of position (quote currency)
            vol: Decimal
                opening fee of position (quote currency)
            vol_closed: Decimal
                position volume closed (base currency unless viqc set in oflags)
            margin: Decimal
                initial margin (quote currency)
            value: typing.Optional[Decimal]
                current value of remaining position (if docalcs requested)(quote currency)
            net: typing.Optional[Decimal]
                unrealized profit/loss of remaining position (if docalcs requested)(quote currency)
            misc: List[str]
                comma delimited list of miscellaneous info
            oflags: str
                 comma delimited list of order flags
            terms: str
            rollovertm: Decimal
   """

    def __call__(self, **kwargs):
        model = _generate_model(list(kwargs.keys()))
        print("\nFields", model.__fields__, "\n")
        return model(**kwargs)