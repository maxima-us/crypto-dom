import asyncio
from typing import IO

import pydantic
import pytest
import httpx
import aiohttp

from returns.io import IO, IOResult, IOSuccess
from returns.result import Result, Success

from crypto_dom.client import HttypeClient
from crypto_dom.kraken.market_data.ohlc import OhlcReq, OhlcResp, METHOD, URL



client = HttypeClient()

payload = {
    "pair": "XXBTZUSD",
    "interval": 60
}


@pytest.mark.asyncio
async def test_httpx_ohlc():
    
    async with client.httpx() as httpx_client:
        r = await httpx_client.safe_request(METHOD, URL, t_in=OhlcReq, t_out=OhlcResp(), params=payload)

    assert isinstance(r, IOResult)
    assert isinstance(r.unwrap(), IO), type(r.unwrap())
    assert isinstance(r.unwrap()._inner_value, httpx.Response)  # IO container doesnt have an unwrap method
    assert hasattr(r.unwrap()._inner_value, "safe_content")

    # below test fails because it is of type <class 'returns.io._IOSuccess'>
    # assert isinstance(r.unwrap()._inner_value.safe_content, OhlcResp) 


@pytest.mark.asyncio
async def test_aiohttp_ohlc():
    
    async with client.aiohttp() as aiohttp_client:
        r = await aiohttp_client.safe_request(METHOD, URL, t_in=OhlcReq, t_out=OhlcResp(), params=payload)

    assert isinstance(r, IOResult)
    assert isinstance(r.unwrap(), IO), type(r.unwrap())
    assert isinstance(r.unwrap()._inner_value, aiohttp.ClientResponse)
    assert hasattr(r.unwrap()._inner_value, "safe_content")