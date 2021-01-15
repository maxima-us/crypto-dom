import asyncio
from typing import IO

import pydantic
import pytest
import httpx

from returns.io import IOResult, IOSuccess

from crypto_dom.client import HttypeClient
from crypto_dom.kraken.ohlc import _OhlcReq, _OhlcResp, METHOD, URL

client = HttypeClient()
payload = {
    "pair": "XXBTZUSD",
    "interval": 60
}


@pytest.mark.asyncio
async def test_ohlc():
    r = await client.safe_request(METHOD, URL, t_in=_OhlcReq, t_out=_OhlcResp("XXBTZUSD"), params=payload)

    assert isinstance(r, IOResult)
    assert isinstance(r.unwrap()._inner_value, httpx.Response)


    assert isinstance(r.unwrap()._inner_value.safe_content._inner_value, pydantic.BaseModel)
