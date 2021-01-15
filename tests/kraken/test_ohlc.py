import random

import pytest
import httpx

from crypto_dom.kraken.ohlc import _OhlcReq, _OhlcResp, METHOD, URL
from crypto_dom.kraken.definitions import TIMEFRAMES




client = httpx.AsyncClient()


payload = {
    "pair": "XXBTZUSD",
    "interval": random.choice(TIMEFRAMES.__args__)
}


@pytest.mark.asyncio
async def test_manual_ohlc():

    print(payload)
    r = await client.request(METHOD, URL, params=payload)
    rjson = r.json()
    assert r.status_code == 200
    assert rjson["error"] == []
    
    # TODO update once we have a full Result model for Kraken
    model = _OhlcResp("XXBTZUSD")
    model(**(rjson["result"]))