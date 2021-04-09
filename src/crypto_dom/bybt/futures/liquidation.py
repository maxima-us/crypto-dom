import typing
from decimal import Decimal

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.bybt.definitions import SYMBOL, EXCHANGE


# ============================================================
# Liquidation Chart
# ============================================================


# doc: https://bybt.gitbook.io/bybt/futures/liquidation

URL = "https://open-api.bybt.com/api/pro/v1/futures/liquidation_chart"
METHOD = "GET"


# ------------------------------
# Request Model
# ------------------------------


class Request(pydantic.BaseModel):
    """Request Model for endpoint https://open-api.bybt.com/api/pro/v1/futures/liquidation_chart

    Model Fields:
    -------------
        exName: str
            Exchange Name (optional)
        symbol: str
            Symbol (optional)
    """

    exName: typing.Optional[EXCHANGE]
    symbol: typing.Optional[SYMBOL]


# ------------------------------
# Response Model
# ------------------------------


class _LiquidationResp(pydantic.BaseModel):

    priceList: typing.Tuple[Decimal, ...]
    sellList: typing.Tuple[Decimal, ...]
    buyList: typing.Tuple[Decimal, ...]
    volList: typing.Tuple[Decimal, ...]
    numList: typing.Tuple[int, ...]
    dateList: typing.Tuple[int, ...]


class Response:
    """Response Model for endpoint https://api.kraken.com/0/private/Balance

    Model Fields:
    -------------
        priceList: List[Decimal]
            Values of asset prices
        sellList:
            Values of total long liquidations
        buyList: 
            Values of total short liquidations
        volList:
            Values of total liquidations
        numList:
            Number of traders liquidated (presumably)
        dateList:
            Timestamps
    """

    def __new__(_cls):
        return _LiquidationResp






# ======================================== 
# TEST

import asyncio
from crypto_dom.client import HttypeClient
from crypto_dom.bybt import BybtFull

if __name__ == "__main__":

    async def liqs():

        async with HttypeClient.httpx() as client:

            headers = {"bybtSecret": "d0ad99c4005e493bb4e7b033a8415109"}
            payload = {"symbol": "BTC"}
            r = await client.safe_request(METHOD, URL, t_in=Request, t_out=BybtFull(Response()), headers=headers, params=payload)
            print(r.value.safe_content)

    
    asyncio.run(liqs())