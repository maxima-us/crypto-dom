import asyncio

from crypto_dom.client import HttypeClient
from crypto_dom.kraken import KrakenFullResponse
from crypto_dom.kraken.market_data.ohlc import METHOD, URL, Request, Response as OHLCResponse


payload = {
    "pair": "XXBTZUSD",
    "interval": 60
}


async def safe_ohlc():

    async with HttypeClient.httpx() as client:
        r = await client.safe_request(METHOD, URL, t_in=Request, t_out=KrakenFullResponse(OHLCResponse()), params=payload)
        
        # r is wrapped inside a result, "value" attribute will gives us the inner value
        if r.is_ok():
            # gives us access to all the same methods and properties as regular httpx client
            rjson = r.value.json()
            rstatus = r.value.status_code

            # extra property "safe_content"
            print(r.value.safe_content)

        else:
            # print error
            print(r.value)

asyncio.run(safe_ohlc())