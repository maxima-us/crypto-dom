import random

import pytest
import httpx

from crypto_dom.kraken.trades import TradesReq, TradesResp, METHOD, URL




client = httpx.AsyncClient()


payload = {
    "pair": "XXBTZUSD",
}


@pytest.mark.asyncio
async def test_manual_trades():

    print("Payload", payload)
    r = await client.request(METHOD, URL, params=payload)
    rjson = r.json()
    assert r.status_code == 200
    assert rjson["error"] == []

    # TODO update once we have a full Result model for Kraken
    model = TradesResp("XXBTZUSD")
    model(**(rjson["result"]))