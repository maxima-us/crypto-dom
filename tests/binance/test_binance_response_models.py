import pytest
import httpx
import time

import stackprinter
stackprinter.set_excepthook(style="darkbg2")

# Public endpoints
from crypto_dom.binance.market_data.aggtrades import Response as AggTradesResp, URL as AggTradesURL
from crypto_dom.binance.market_data.average_price import Response as AvgPriceResp, URL as AvgPriceURL
from crypto_dom.binance.market_data.depth import Response as DepthResp, URL as DepthURL
from crypto_dom.binance.market_data.exchange_info import Response as ExchInfoResp, URL as ExchInfoURL
from crypto_dom.binance.market_data.historical_trades import Response as HTradesResp, URL as HTradesURL
from crypto_dom.binance.market_data.klines import Response as KlinesResp, URL as KlinesURL
from crypto_dom.binance.market_data.orderbook_ticker import Response as OBTickerResp, URL as OBTickerURL
from crypto_dom.binance.market_data.price_ticker import Response as PTickerResp, URL as PTickerURL
from crypto_dom.binance.market_data.trades import Response as TradesResp, URL as TradesURL


# CONSTANTS
symbol = "BTCUSDT"
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

    # TODO write binance auth
    headers = {}


    async with httpx.AsyncClient() as client:
        if method in ["POST"]:
            r = await client.request(method, url, data=payload, headers=headers)
        else:
            r = await client.request(method, url, params=payload)
        
        rjson = r.json()
        # print("response.json", rjson)

        assert r.status_code == 200

        if isinstance(rjson, list) or isinstance(rjson, tuple):
            response_model(rjson)
        else:
            response_model(**rjson)

        return rjson


#------------------------------------------------------------
# Public Endpoints
#------------------------------------------------------------


@pytest.mark.asyncio
@pytest.mark.default_cassette("public/test_aggtrades_response_model.yaml")
@pytest.mark.vcr()
async def test_aggtrades_response_model():
    payload = {"symbol": symbol}
    await _httpx_request("GET", AggTradesURL, payload, AggTradesResp())


@pytest.mark.asyncio
@pytest.mark.default_cassette("public/test_average_price_response_model.yaml")
@pytest.mark.vcr()
async def test_average_price_response_model():
    payload = {"symbol": symbol}
    await _httpx_request("GET", AvgPriceURL, payload, AvgPriceResp())


@pytest.mark.asyncio
@pytest.mark.default_cassette("public/test_depth_response_model.yaml")
@pytest.mark.vcr()
async def test_depth_response_model():
    payload = {"symbol": symbol}
    await _httpx_request("GET", DepthURL, payload, DepthResp())


@pytest.mark.asyncio
@pytest.mark.default_cassette("public/test_exchange_info_response_model.yaml")
@pytest.mark.vcr()
async def test_exchange_info_response_model():
    payload = {}
    await _httpx_request("GET", ExchInfoURL, payload, ExchInfoResp())


# ! REQUIRES API KEY (X-MBX-APIKEY as defined in doc)
# @pytest.mark.asyncio
# @pytest.mark.default_cassette("public/test_historical_trades_response_model.yaml")
# @pytest.mark.vcr()
# async def test_historical_trades_response_model():
#     payload = {"symbol": symbol}
#     await _httpx_request("GET", HTradesURL, payload, HTradesResp())


@pytest.mark.asyncio
@pytest.mark.default_cassette("public/test_klines_response_model.yaml")
@pytest.mark.vcr()
async def test_klines_response_model():
    payload = {"symbol": symbol, "interval": "15m"}
    await _httpx_request("GET", KlinesURL, payload, KlinesResp())


@pytest.mark.asyncio
@pytest.mark.default_cassette("public/test_obticker_response_model.yaml")
@pytest.mark.vcr()
async def test_obticker_response_model():
    payload = {"symbol": symbol}


    async with httpx.AsyncClient() as client:
        r = await client.request("GET", OBTickerURL, params=payload)
        
        rjson = r.json()

        assert r.status_code == 200
        _model = OBTickerResp()
        _model(rjson)


@pytest.mark.asyncio
@pytest.mark.default_cassette("public/test_pticker_response_model.yaml")
@pytest.mark.vcr()
async def test_pticker_response_model():
    payload = {"symbol": symbol}
    
    async with httpx.AsyncClient() as client:
        r = await client.request("GET", PTickerURL, params=payload)
        
        rjson = r.json()

        assert r.status_code == 200
        _model = PTickerResp()
        _model(rjson)


@pytest.mark.asyncio
@pytest.mark.default_cassette("public/test_trades_response_model.yaml")
@pytest.mark.vcr()
async def test_trades_response_model():
    payload = {"symbol": symbol}
    await _httpx_request("GET", TradesURL, payload, TradesResp())


#------------------------------------------------------------
# Private Endpoints 
# ! FROM KRAKEN = NOT YET UPDATED
#------------------------------------------------------------


# @pytest.mark.asyncio
# # @pytest.mark.default_cassette("private/test_accountbalance_response_model.yaml")
# # @pytest.mark.vcr()
# async def test_accountbalance_response_model():
#     payload = {"nonce": make_nonce()}
#     await _httpx_request("POST", ABURL, payload, AccountBalanceResp())


# @pytest.mark.asyncio
# # @pytest.mark.default_cassette("private/test_tradebalance_response_model.yaml")
# # @pytest.mark.vcr()
# async def test_tradebalance_response_model():
#     payload = {"nonce": make_nonce(), "asset": asset}
#     await _httpx_request("POST", TBURL, payload, TradeBalanceResp())


# @pytest.mark.asyncio
# # @pytest.mark.default_cassette("private/test_closedorders_response_model.yaml")
# # @pytest.mark.vcr()
# async def test_closedorders_response_model():
#     payload = {"nonce": make_nonce()}
#     await _httpx_request("POST", COURL, payload, ClosedOrdersResp())


# @pytest.mark.asyncio
# # @pytest.mark.default_cassette("private/test_openpositions_response_model.yaml")
# # @pytest.mark.vcr()
# async def test_openpositions_response_model():
#     payload = {"nonce": make_nonce()}
#     await _httpx_request("POST", OPURL, payload, OpenPositionsResp())


# @pytest.mark.asyncio
# # @pytest.mark.default_cassette("private/test_openorders_response_model.yaml")
# # @pytest.mark.vcr()
# async def test_openorders_response_model():
#     payload = {"nonce": make_nonce()}
#     await _httpx_request("POST", OOURL, payload, OpenOrdersResp())


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


# @pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_tradeshistory_response_model.yaml")
# @pytest.mark.vcr()
# async def test_tradeshistory_response_model():
#     payload = {"nonce": make_nonce()}
#     await _httpx_request("POST", THURL, payload, TradesHistoryResp())


#------------------------------------------------------------
# Record Cassettes
#------------------------------------------------------------


if __name__ == '__main__':
    pytest.main(['-s', __file__, '--block-network'])
    # To record cassettes uncomment below line
    # pytest.main(['-s', __file__, '--record-mode=new_episodes'])