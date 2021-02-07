import asyncio

import httpx
from pydantic import ValidationError

from crypto_dom.kraken import KrakenFullResponse
from crypto_dom.kraken.market_data.ohlc import METHOD, URL, Request, Response as OHLCResponse


payload = {
    "pair": "XXBTZUSD",
    "interval": 60
}


try:
    valid_req = Request(**payload)
except ValidationError as e:
    raise e

async def ohlc():
    async with httpx.AsyncClient() as client:
        r = await client.request(METHOD, URL, params=valid_req.dict(exclude_none=True))
        rjson = r.json()

        # instantiate model
        resp_model = KrakenFullResponse(OHLCResponse())

        # pass decoded JSON response content to model to validate
        # Note: do not unpack as you usually would for pydantic models !
        try:
            valid_resp = resp_model(rjson)
            print(valid_resp.value)
        except ValidationError as e:
            raise e


asyncio.run(ohlc())