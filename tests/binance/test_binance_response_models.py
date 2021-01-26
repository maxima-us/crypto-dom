from urllib.parse import urlencode
import pydantic
import pytest
import httpx
import time

import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from typing_extensions import Literal

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

# Auth
from crypto_dom.binance.__sign import get_keys, auth_signature, auth_headers, auth_timestamp, EmptyEnv

# Private Endpoints
## Wallet
from crypto_dom.binance.wallet.withdraw_history import Response as WiHiResp, URL as WiHiURL
from crypto_dom.binance.wallet.deposit_history import Response as DepHiResp, URL as DepHiURL
from crypto_dom.binance.wallet.getall import Response as GetAllResp, URL as GetAllURL
from crypto_dom.binance.wallet.account_snapshot import Response as AccSnapResp, URL as AccSnapURL
from crypto_dom.binance.wallet.asset_dividend import Response as ADivResp, URL as ADivURL
from crypto_dom.binance.wallet.deposit_address import Response as DepAdResp, URL as DepAdURL

## Spot Account
from crypto_dom.binance.spot_account.account_information import Response as AccInfoResp, URL as AccInfoURL
from crypto_dom.binance.spot_account.account_trade_list import Response as AccTrLResp, URL as AccTrLURL
from crypto_dom.binance.spot_account.all_orders import Response as AllOResp, URL as AllOURL
from crypto_dom.binance.spot_account.open_orders import Response as OpenOResp, URL as OpenOURL
from crypto_dom.binance.spot_account.query_all_oco import Response as AllOCOResp, URL as AllOCOURL
from crypto_dom.binance.spot_account.query_open_oco import Response as OpenOCOResp, URL as OpenOCOURL
from crypto_dom.binance.spot_account.test_new_order import Response as TestNewOResp, URL as TestNewOURL


# CONSTANTS
symbol = "BTCUSDT"
asset = "DOT"
coin = "DOT"


def make_nonce():
    return int(time.time()*10**3)


#------------------------------------------------------------
# Base
#------------------------------------------------------------


async def _httpx_request(method: Literal["GET", "POST", "DELETE"], url: str, payload: dict, response_model: pydantic.BaseModel, private: bool=False):
    """tuples of (url, payload)
    """
    # return

    if private:
        try:
            keyset = get_keys() # returns a set of tuples (key, secret) 
        except EmptyEnv:
            # do not proceed to send a test request in this case
            return
        key, secret = keyset.pop()
        payload["timestamp"] = auth_timestamp()
        payload["signature"] = auth_signature(url, payload, secret=secret)
        headers = auth_headers(key)
    else:
        headers = {}

    async with httpx.AsyncClient() as client:
        if private:
            signature = payload.pop("signature")
            payload = sorted([(k, v) for k, v in payload.items()], reverse=False)
            payload.append(("signature", signature))    #! needs to always be last param
            if method in ["POST", "DELETE"]:
                r = await client.request(method, url, data=dict(payload), headers=headers)
            else:
                r = await client.request(method, url, params=payload, headers=headers)
        else:
            r = await client.request(method, url, params=payload)
        
        rjson = r.json()
        print("response.json", rjson)

        assert r.status_code == 200, f"Json Response {rjson} \nPayload {payload} \nHeaders {headers} \nRequest {r.request}"

        # if empty response, return directly without validation
        # (this might be what we expected, so assertion has to take place in the test function not here)
        if not rjson:
            return rjson

        # else we validate
        if isinstance(rjson, list) or isinstance(rjson, tuple):
            response_model(rjson)
        else:
            response_model(**rjson)


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


@pytest.mark.asyncio
@pytest.mark.default_cassette("public/test_historical_trades_response_model.yaml")
@pytest.mark.vcr()
async def test_historical_trades_response_model():
    payload = {"symbol": symbol}

    # ! REQUIRES API KEY (X-MBX-APIKEY as defined in doc)
    try:
        keyset = get_keys() # returns a set of tuples (key, secret) 
    except EmptyEnv:
        # do not proceed to send a test request in this case
        return
    key, _ = keyset.pop()
    headers = auth_headers(key)

    async with httpx.AsyncClient() as client:
        r = await client.request("GET", HTradesURL, params=payload, headers=headers)
        
        rjson = r.json()

        assert r.status_code == 200, f"JSON Response {rjson} --- Payload {payload} --- Headers {headers}"
        _model = HTradesResp()
        _model(rjson)


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

        assert r.status_code == 200, rjson
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

        assert r.status_code == 200, rjson
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
#------------------------------------------------------------

# ------ Wallet

@pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_withdrawhistory_response_model.yaml")
# @pytest.mark.vcr()
async def test_withdrawhistory_response_model():
    payload = {"coin": coin}
    await _httpx_request("GET", WiHiURL, payload, WiHiResp(), private=True)


@pytest.mark.asyncio
# # @pytest.mark.default_cassette("private/test_deposithistory_response_model.yaml")
# # @pytest.mark.vcr()
async def test_deposithistory_response_model():
    payload = {"coin": coin}
    await _httpx_request("GET", DepHiURL, payload, DepHiResp(), private=True)


@pytest.mark.asyncio
# # @pytest.mark.default_cassette("private/test_getall_response_model.yaml")
# # @pytest.mark.vcr()
async def test_getall_response_model():
    payload = {}
    await _httpx_request("GET", GetAllURL, payload, GetAllResp(), private=True)


@pytest.mark.asyncio
# # @pytest.mark.default_cassette("private/test_accountsnapshot_response_model.yaml")
# # @pytest.mark.vcr()
async def test_accountsnapshot_response_model():
    payload = {"type": "SPOT"}
    await _httpx_request("GET", AccSnapURL, payload, AccSnapResp(), private=True)


@pytest.mark.asyncio
# # @pytest.mark.default_cassette("private/test_assetdividend_response_model.yaml")
# @pytest.mark.vcr()
async def test_assetdividend_response_model():
    payload = {"asset": coin}
    await _httpx_request("GET", ADivURL, payload, ADivResp(), private=True)


@pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_depositaddress_response_model.yaml")
# @pytest.mark.vcr()
async def test_depositaddress_response_model():
    payload = {"coin": coin}
    await _httpx_request("GET", DepAdURL, payload, DepAdResp(), private=True)



# ------ Spot Account

@pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_accountinformation_response_model.yaml")
# @pytest.mark.vcr()
async def test_accountinformation_response_model():
    payload = {}
    await _httpx_request("GET", AccInfoURL, payload, AccInfoResp(), private=True)


@pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_accounttradelist_response_model.yaml")
# @pytest.mark.vcr()
async def test_accounttradelist_response_model():
    payload = {"symbol": symbol}
    await _httpx_request("GET", AccTrLURL, payload, AccTrLResp(), private=True)


@pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_allorders_response_model.yaml")
# @pytest.mark.vcr()
async def test_allorders_response_model():
    payload = {"symbol": symbol}
    await _httpx_request("GET", AllOURL, payload, AllOResp(), private=True)
    

@pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_openorders_response_model.yaml")
# @pytest.mark.vcr()
async def test_openorders_response_model():
    payload = {"symbol": symbol}
    await _httpx_request("GET", OpenOURL, payload, OpenOResp(), private=True)


@pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_queryallOCO_response_model.yaml")
# @pytest.mark.vcr()
async def test_allOCOorders_response_model():
    payload = {}
    await _httpx_request("GET", AllOCOURL, payload, AllOCOResp(), private=True)


@pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_queryopenOCO_response_model.yaml")
# @pytest.mark.vcr()
async def test_openOCOorders_response_model():
    payload = {}
    await _httpx_request("GET", OpenOCOURL, payload, OpenOCOResp(), private=True)


@pytest.mark.asyncio
# @pytest.mark.default_cassette("private/test_testneworder_response_model.yaml")
# @pytest.mark.vcr()
async def test_testneworder_response_model():
    payload = {
        "symbol": symbol,
        "side": "BUY",
        "timeInForce": "GTC",
        "quantity": 0.01,
        "price": 30000,
        "type": "LIMIT"
    }
    r = await _httpx_request("POST", TestNewOURL, payload, TestNewOResp(), private=True)
    assert r == {}


#------------------------------------------------------------
# Record Cassettes
#------------------------------------------------------------


if __name__ == '__main__':
    # pytest.main(['-s', __file__, '--block-network'])
    # To record cassettes uncomment below line
    pytest.main(['-s', __file__, '--record-mode=new_episodes'])