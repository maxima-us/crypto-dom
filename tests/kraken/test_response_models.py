import pytest
import httpx
import time

# Public endpoints
from crypto_dom.kraken.ohlc import OhlcResp, URL as OHLCURL
from crypto_dom.kraken.orderbook import OrderBookResp, URL as OBURL
from crypto_dom.kraken.asset_pairs import AssetPairsResp, URL as APURL
from crypto_dom.kraken.assets import AssetsResp, URL as AURL
from crypto_dom.kraken.ticker import TickerResp, URL as TURL
from crypto_dom.kraken.spread import SpreadResp, URL as SURL

# Auth
from crypto_dom.kraken.__sign import get_keys, auth_headers, EmptyEnv

# Private endpoints
from crypto_dom.kraken.account_balance import AccountBalanceResp, URL as ABURL
from crypto_dom.kraken.trade_balance import TradeBalanceResp, URL as TBURL
from crypto_dom.kraken.open_positions import OpenPositionsResp, URL as OPURL
from crypto_dom.kraken.open_orders import OpenOrdersResp, URL as OOURL
from crypto_dom.kraken.closed_orders import ClosedOrdersResp, URL as COURL
from crypto_dom.kraken.query_orders import QueryOrdersResp, URL as QOURL
from crypto_dom.kraken.query_ledgers import QueryLedgersResp, URL as QLURL
from crypto_dom.kraken.query_trades import QueryTradesResp, URL as QTURL
from crypto_dom.kraken.trades_history import TradesHistoryResp, URL as THURL


# CONSTANTS
pair = "XXBTZUSD"
pairs = ["XXBTZUSD", "XETHZUSD", "XZECZUSD"]
asset = "XETH"
assets = ["XXBT", "XETH", "XTZ"]


def make_nonce():
    return int(time.time()*10**3)


#------------------------------------------------------------
# Base
#------------------------------------------------------------


async def _httpx_request(method, url, payload, response_model):
    """tuples of (url, payload)
    """
    # return

    if method in ["POST"]:
        try:
            keyset = get_keys() # returns a set of tuples (key, secret) 
        except EmptyEnv:
            # do not proceed to send a test request in this case
            return
        key, secret = keyset.pop()
        headers = auth_headers(url, payload, key=key, secret=secret)
    else:
        headers = {}

    async with httpx.AsyncClient() as client:
        if method in ["POST"]:
            r = await client.request(method, url, data=payload, headers=headers)
        else:
            r = await client.request(method, url, params=payload)
        
        rjson = r.json()
        print("response.json", rjson)

        assert r.status_code == 200
        assert rjson["error"] == []

        result = rjson["result"]
        response_model(**result)

        return result


#------------------------------------------------------------
# Public Endpoints
#------------------------------------------------------------


@pytest.mark.asyncio
async def test_ohlc_response_model():
    payload = {"pair": pair}
    await _httpx_request("GET", OHLCURL, payload, OhlcResp(pair))


@pytest.mark.asyncio
async def test_orderbook_response_model():
    payload = {"pair": pair}
    await _httpx_request("GET", OBURL, payload, OrderBookResp(pair))


@pytest.mark.asyncio
async def test_assetpairs_response_model():
    payload = {"pair": pairs}
    await _httpx_request("GET", APURL, payload, AssetPairsResp())


@pytest.mark.asyncio
async def test_assets_response_model():
    payload = {"asset": assets}
    await _httpx_request("GET", AURL, payload, AssetsResp())


@pytest.mark.asyncio
async def test_ticker_response_model():
    payload = {"pair": pairs}
    await _httpx_request("GET", TURL, payload, TickerResp())


@pytest.mark.asyncio
async def test_spread_response_model():
    payload = {"pair": pair}
    await _httpx_request("GET", SURL, payload, SpreadResp(pair))


#------------------------------------------------------------
# Private Endpoints
#------------------------------------------------------------


@pytest.mark.asyncio
async def test_accountbalance_response_model():
    payload = {"nonce": make_nonce()}
    await _httpx_request("POST", ABURL, payload, AccountBalanceResp())


@pytest.mark.asyncio
async def test_tradebalance_response_model():
    payload = {"nonce": make_nonce(), "asset": asset}
    await _httpx_request("POST", TBURL, payload, TradeBalanceResp())


@pytest.mark.asyncio
async def test_closedorders_response_model():
    payload = {"nonce": make_nonce()}
    await _httpx_request("POST", COURL, payload, ClosedOrdersResp())


@pytest.mark.asyncio
async def test_openpositions_response_model():
    payload = {"nonce": make_nonce()}
    await _httpx_request("POST", OPURL, payload, OpenPositionsResp())


@pytest.mark.asyncio
async def test_openorders_response_model():
    payload = {"nonce": make_nonce()}
    await _httpx_request("POST", OOURL, payload, OpenOrdersResp())


# TODO which IDs to query ?
# @pytest.mark.asyncio
# async def test_queryorders_response_model():
#     payload = {"nonce": make_nonce()}
#     await _httpx_request("POST", QOURL, payload, QueryOrdersResp())


# TODO which IDs to query ?
# @pytest.mark.asyncio
# async def test_queryledgers_response_model():
#     payload = {"nonce": make_nonce()}
#     await _httpx_request("POST", QLURL, payload, QueryLedgersResp())


# # TODO which IDs to query ?
# @pytest.mark.asyncio
# async def test_querytrades_response_model():
#     payload = {"nonce": make_nonce()}
#     await _httpx_request("POST", QTURL, payload, QueryTradessResp()


@pytest.mark.asyncio
async def test_tradeshistory_response_model():
    payload = {"nonce": make_nonce()}
    await _httpx_request("POST", THURL, payload, TradesHistoryResp())