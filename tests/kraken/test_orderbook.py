import random

import pytest
import httpx

from crypto_dom.kraken.orderbook import OrderBookReq, OrderBookResp, METHOD, URL




client = httpx.AsyncClient()


payload = {
    "pair": "XXBTZUSD",
    "count": random.randint(0, 1000)
}


@pytest.mark.asyncio
async def test_manual_book():

    print("Payload", payload)
    r = await client.request(METHOD, URL, params=payload)
    rjson = r.json()
    assert r.status_code == 200
    assert rjson["error"] == []

    # TODO update once we have a full Result model for Kraken
    model = OrderBookResp("XXBTZUSD")
    model(**(rjson["result"]))