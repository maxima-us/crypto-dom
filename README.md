# crypto-dom

Modeling of crypto exchanges domains

For each endpoint, we provide the full URL path, URL method, a Request model (to validate query parameters) and a Response model.

<br>

### Basic Usage

#### Models

```python
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
```

#### Client

```python
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
```
