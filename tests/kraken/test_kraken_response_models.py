import pytest
import httpx
import time

# Public endpoints
from crypto_dom.kraken.market_data.ohlc import Response as OhlcResp, URL as OHLCURL
from crypto_dom.kraken.market_data.orderbook import Response as OrderBookResp, URL as OBURL
from crypto_dom.kraken.market_data.asset_pairs import Response as AssetPairsResp, URL as APURL
from crypto_dom.kraken.market_data.assets import Response as AssetsResp, URL as AURL
from crypto_dom.kraken.market_data.ticker import Response as TickerResp, URL as TURL
from crypto_dom.kraken.market_data.spread import Response as SpreadResp, URL as SURL

# Auth
from crypto_dom.kraken.__sign import get_keys, auth_headers, EmptyEnv

# Private endpoints
from crypto_dom.kraken.user_data.account_balance import Response as AccountBalanceResp, URL as ABURL
from crypto_dom.kraken.user_data.trade_balance import Response as TradeBalanceResp, URL as TBURL
from crypto_dom.kraken.user_data.open_positions import Response as OpenPositionsResp, URL as OPURL
from crypto_dom.kraken.user_data.open_orders import Response as OpenOrdersResp, URL as OOURL
from crypto_dom.kraken.user_data.closed_orders import Response as ClosedOrdersResp, URL as COURL
from crypto_dom.kraken.user_data.query_orders import Response as QueryOrdersResp, URL as QOURL
from crypto_dom.kraken.user_data.query_ledgers import Response as QueryLedgersResp, URL as QLURL
from crypto_dom.kraken.user_data.query_trades import Response as QueryTradesResp, URL as QTURL
from crypto_dom.kraken.user_data.trades_history import Response as TradesHistoryResp, URL as THURL
from crypto_dom.kraken.user_funding.deposit_methods import Response as DepMetResp, URL as DepMetURL
from crypto_dom.kraken.user_funding.deposit_addresses import Response as DepAddResp, URL as DepAddURL
from crypto_dom.kraken.user_funding.withdraw_info import Response as WdInfoResp, URL as WdInfoURL
from crypto_dom.kraken.user_trading.add_order import Response as AddOrdResp, URL as AddOrdURL


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

        assert r.status_code == 200, f"Response json {rjson}"
        assert rjson["error"] == [], f"Response json {rjson}"

        result = rjson["result"]
        # response_model(**result)  # we want syntax for all endpoints to be the same, so no unpacking (in case we have lists)
        response_model(result)

        return result


#------------------------------------------------------------
# Public Endpoints
#------------------------------------------------------------


@pytest.mark.asyncio
@pytest.mark.default_cassette("public/test_ohlc_response_model.yaml")
@pytest.mark.vcr()
async def test_ohlc_response_model():
    payload = {"pair": pair}
    await _httpx_request("GET", OHLCURL, payload, OhlcResp())


@pytest.mark.asyncio
@pytest.mark.default_cassette("public/test_orderbook_response_model.yaml")
@pytest.mark.vcr()
async def test_orderbook_response_model():
    payload = {"pair": pair}
    await _httpx_request("GET", OBURL, payload, OrderBookResp())


@pytest.mark.asyncio
@pytest.mark.default_cassette("public/test_assetpairs_response_model.yaml")
@pytest.mark.vcr()
async def test_assetpairs_response_model():
    payload = {"pair": pairs}
    await _httpx_request("GET", APURL, payload, AssetPairsResp())


@pytest.mark.asyncio
@pytest.mark.default_cassette("public/test_assets_response_model.yaml")
@pytest.mark.vcr()
async def test_assets_response_model():
    payload = {"asset": assets}
    await _httpx_request("GET", AURL, payload, AssetsResp())


@pytest.mark.asyncio
@pytest.mark.default_cassette("public/test_ticker_response_model.yaml")
@pytest.mark.vcr()
async def test_ticker_response_model():
    payload = {"pair": pairs}
    await _httpx_request("GET", TURL, payload, TickerResp())


@pytest.mark.asyncio
@pytest.mark.default_cassette("public/test_spread_response_model.yaml")
@pytest.mark.vcr()
async def test_spread_response_model():
    payload = {"pair": pair}
    await _httpx_request("GET", SURL, payload, SpreadResp())


#------------------------------------------------------------
# Private Endpoints
#------------------------------------------------------------

# ------ User Data

@pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_accountbalance_response_model.yaml")
# @pytest.mark.vcr()
async def test_accountbalance_response_model():
    payload = {"nonce": make_nonce()}
    await _httpx_request("POST", ABURL, payload, AccountBalanceResp())


@pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_tradebalance_response_model.yaml")
# @pytest.mark.vcr()
async def test_tradebalance_response_model():
    payload = {"nonce": make_nonce(), "asset": asset}
    await _httpx_request("POST", TBURL, payload, TradeBalanceResp())


@pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_closedorders_response_model.yaml")
# @pytest.mark.vcr()
async def test_closedorders_response_model():
    payload = {"nonce": make_nonce()}
    await _httpx_request("POST", COURL, payload, ClosedOrdersResp())


@pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_openpositions_response_model.yaml")
# @pytest.mark.vcr()
async def test_openpositions_response_model():
    payload = {"nonce": make_nonce()}
    await _httpx_request("POST", OPURL, payload, OpenPositionsResp())


@pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_openorders_response_model.yaml")
# @pytest.mark.vcr()
async def test_openorders_response_model():
    payload = {"nonce": make_nonce()}
    await _httpx_request("POST", OOURL, payload, OpenOrdersResp())


# TODO which IDs to query ?
# @pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_queryorders_response_model.yaml")
# @pytest.mark.vcr()
# async def test_queryorders_response_model():
#     payload = {"nonce": make_nonce()}
#     await _httpx_request("POST", QOURL, payload, QueryOrdersResp())


# TODO which IDs to query ?
# @pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_queryledgers_response_model.yaml")
# @pytest.mark.vcr()
# async def test_queryledgers_response_model():
#     payload = {"nonce": make_nonce()}
#     await _httpx_request("POST", QLURL, payload, QueryLedgersResp())


# # TODO which IDs to query ?
# @pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_querytrades_response_model.yaml")
# @pytest.mark.vcr()
# async def test_querytrades_response_model():
#     payload = {"nonce": make_nonce()}
#     await _httpx_request("POST", QTURL, payload, QueryTradessResp()


@pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_tradeshistory_response_model.yaml")
# @pytest.mark.vcr()
async def test_tradeshistory_response_model():
    payload = {"nonce": make_nonce()}
    await _httpx_request("POST", THURL, payload, TradesHistoryResp())


# ------ User Funding


@pytest.mark.asyncio
async def test_depositmethods_reponse_model():
    payload = {"asset": asset, "nonce": make_nonce()}
    r = await _httpx_request("POST", DepMetURL, payload, DepMetResp())
    print(r)


@pytest.mark.asyncio
async def test_depositaddresses_reponse_model():
    payload = {"asset": asset, "nonce": make_nonce(), "method": "Ether (Hex)"}
    r = await _httpx_request("POST", DepAddURL, payload, DepAddResp())
    print(r)


# ? where to get "key" param
# @pytest.mark.asyncio
# async def test_withdrawinfo_reponse_model():
#     payload = {"asset": asset, "nonce": make_nonce(), "amount": 0.1, "key": "test"}
#     r = await _httpx_request("POST", WdInfoURL, payload, WdInfoResp())
#     print(r)


# @pytest.mark.asyncio
# async def test_addorder_response_model():
#     payload = {
#         "pair": pair,
#         "type": "buy",
#         "price": 10_000,
#         "volume": 0.01,
#         "ordertype": "limit",
#         "nonce": make_nonce(),
#         "_validate": True
#     }
#     r = await _httpx_request("POST", AddOrdURL, payload, AddOrdResp())
#     print(r)



#------------------------------------------------------------
# Record Cassettes
#------------------------------------------------------------


if __name__ == '__main__':
    # pytest.main(['-s', __file__, '--block-network'])
    # To record cassettes uncomment below line
    pytest.main(['-s', __file__, '--record-mode=new_episodes'])