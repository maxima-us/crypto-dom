import pytest
import httpx

from crypto_dom.kraken.ohlc import OhlcResp, URL as OHLCURL
from crypto_dom.kraken.orderbook import OrderBookResp, URL as OBURL
from crypto_dom.kraken.asset_pairs import AssetPairsResp, URL as APURL
from crypto_dom.kraken.assets import AssetsResp, URL as AURL
from crypto_dom.kraken.ticker import TickerResp, URL as TURL
from crypto_dom.kraken.spread import SpreadResp, URL as SURL


# CONSTANTS
pair = "XXBTZUSD"
pairs = ["XXBTZUSD", "XETHZUSD", "XZECZUSD"]
assets = ["XXBT", "XETH", "XTZ"]


async def _httpx_request(url, payload, response_model):
    """tuples of (url, payload)
    """
    async with httpx.AsyncClient() as client:
            r = await client.get(url, params=payload)
            rjson = r.json()
            print("response.json", rjson)
            result = rjson["result"]

            assert r.status_code == 200
            assert rjson["error"] == []

            response_model(**result)


@pytest.mark.asyncio
async def test_ohlc_response_model():
    payload = {"pair": pair}
    await _httpx_request(OHLCURL, payload, OhlcResp(pair))


@pytest.mark.asyncio
async def test_orderbook_response_model():
    payload = {"pair": pair}
    await _httpx_request(OBURL, payload, OrderBookResp(pair))


@pytest.mark.asyncio
async def test_assetpairs_response_model():
    payload = {"pair": pairs}
    await _httpx_request(APURL, payload, AssetPairsResp())


@pytest.mark.asyncio
async def test_assets_response_model():
    payload = {"asset": assets}
    await _httpx_request(AURL, payload, AssetsResp())


@pytest.mark.asyncio
async def test_ticker_response_model():
    payload = {"pair": pairs}
    await _httpx_request(TURL, payload, TickerResp())


@pytest.mark.asyncio
async def test_spread_response_model():
    payload = {"pair": pair}
    await _httpx_request(SURL, payload, SpreadResp(pair))