import random
import asyncio
from _pytest import python

import pytest
import httpx

from hypothesis import given, settings
from hypothesis_jsonschema import from_schema

from crypto_dom.kraken.ohlc import OhlcReq, OhlcResp, METHOD, URL
from crypto_dom.kraken.definitions import TIMEFRAME




client = httpx.AsyncClient()


payload = {
    "pair": "XXBTZUSD",
    "interval": random.choice(TIMEFRAME.__args__)
}



@pytest.mark.asyncio
async def test_manual_ohlc():

    print(payload)
    r = await client.request(METHOD, URL, params=payload)
    rjson = r.json()
    assert r.status_code == 200
    assert rjson["error"] == []
    
    # TODO update once we have a full Result model for Kraken
    model = OhlcResp("XXBTZUSD")
    model(**(rjson["result"]))




#------------------------------------------------------------
# FIXME max_examples argument doesnt seem to work
#------------------------------------------------------------


# testcases = 0
# # dont generate pair as this WILL fail all the time 

# schema = _OhlcReq.schema()
# test_schema = {k: v for k, v in _OhlcReq.schema().items() if k not in ["pair"]}

# @given(from_schema(test_schema))
# @settings(deadline=None, max_examples=5)
# @pytest.mark.asyncio
# async def test_property_ohlc(generated_payload):

#     global testcases
#     testcases += 1
#     print("Tested Cases", testcases)

#     # replace generated pair
#     generated_payload["pair"] = "XXBTZUSD"

#     r = await client.request(METHOD, URL, params=generated_payload)
#     rjson = r.json()
#     assert r.status_code == 200
#     assert rjson["error"] == []

#     await asyncio.sleep(random.randint(3, 6))

