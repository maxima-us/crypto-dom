import pytest
import aiohttp
import httpx

from crypto_dom.result import Result
from crypto_dom.client import HttypeClient
from crypto_dom.kraken import ErrorResponse, KrakenFullResponse
from crypto_dom.kraken.market_data.ohlc import Request, Response, METHOD, URL



client = HttypeClient()

payload = {
    "pair": "XXBTZUSD",
    "interval": 60
}


@pytest.mark.asyncio
async def test_httpx_ohlc():
    
    async with client.httpx() as httpx_client:
        r = await httpx_client.safe_request(METHOD, URL, t_in=Request, t_out=KrakenFullResponse(Response()), params=payload)

    assert r.is_ok(), r.value
    assert r.value.status_code == 200
    assert isinstance(r.value, httpx.Response)
    assert r.value.safe_content.is_ok()
    assert "XXBTZUSD" in r.value.safe_content.value.__fields__
    assert "last" in r.value.safe_content.value.__fields__



@pytest.mark.asyncio
async def test_aiohttp_ohlc():
    
    async with client.aiohttp() as aiohttp_client:
        r = await aiohttp_client.safe_request(METHOD, URL, t_in=Request, t_out=KrakenFullResponse(Response()), params=payload)

    assert r.is_ok(), r.value
    assert r.value.status == 200
    assert isinstance(r.value, aiohttp.ClientResponse)
    assert r.value.safe_content.is_ok()
    assert "XXBTZUSD" in r.value.safe_content.value.__fields__
    assert "last" in r.value.safe_content.value.__fields__