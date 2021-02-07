
import random
import asyncio

import stackprinter
stackprinter.set_excepthook(style="darkbg2")
import pytest
import httpx
from hypothesis import given, settings
from hypothesis_jsonschema import from_schema

from crypto_dom.kraken import KrakenFullResponse
from crypto_dom.hypothesis_settings import DEADLINE, MAX_EXAMPLES, SUPPRESS_HEALTH_CHECK, VERBOSITY




#------------------------------------------------------------
# HYPOTHESIS BASE REQUEST
#------------------------------------------------------------

async def _hypothesis_request(method, url, generated_payload, response_model):

    testcases = 0
    async with httpx.AsyncClient() as client:
        # global testcases
        testcases += 1

        if testcases > 5:
            print("Skipping Test Case")
            assert True

        print("Tested Cases", testcases)
        print("Generated", generated_payload)

        r = await client.request(method, url, params=generated_payload)
        rjson = r.json()

        # validate
        response_model(rjson)

        assert r.status_code == 200, rjson
        assert rjson["error"] == [], r.request

        await asyncio.sleep(random.randint(2, 5))




#------------------------------------------------------------
# HYPOTHESIS TEST OHLC
#------------------------------------------------------------
from crypto_dom.kraken.market_data.ohlc import (
        Request as OHLCRequest,
        Response as OHLCResponse,
        METHOD as OHLCMETHOD,
        URL as OHLCURL
    )

schema = OHLCRequest.schema()
test_schema = {k: v for k, v in OHLCRequest.schema().items()}


@given(from_schema(test_schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_ohlc(generated_payload):

    await _hypothesis_request(OHLCMETHOD, OHLCURL, generated_payload, KrakenFullResponse(OHLCResponse()))



#------------------------------------------------------------
# HYPOTHESIS TEST ORDERBOOK
#------------------------------------------------------------
from crypto_dom.kraken.market_data.orderbook import (
        Request as OBRequest,
        Response as OBResponse,
        METHOD as OBMETHOD,
        URL as OBURL
    )

schema = OBRequest.schema()
test_schema = {k: v for k, v in OBRequest.schema().items()}


@given(from_schema(test_schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_orderbook(generated_payload):

    await _hypothesis_request(OBMETHOD, OBURL, generated_payload, KrakenFullResponse(OBResponse()))



#------------------------------------------------------------
# HYPOTHESIS TEST TRADES
#------------------------------------------------------------
from crypto_dom.kraken.market_data.trades import (
        Request as TradesRequest,
        Response as TradesResponse,
        METHOD as TradesMETHOD,
        URL as TradesURL
    )

schema = TradesRequest.schema()
test_schema = {k: v for k, v in TradesRequest.schema().items()}


@given(from_schema(test_schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_trades(generated_payload):

    await _hypothesis_request(TradesMETHOD, TradesURL, generated_payload, KrakenFullResponse(TradesResponse()))



#------------------------------------------------------------
# HYPOTHESIS TEST SPREAD
#------------------------------------------------------------
from crypto_dom.kraken.market_data.spread import (
        Request as SpreadRequest,
        Response as SpreadResponse,
        METHOD as SpreadMETHOD, 
        URL as SpreadURL
    )

schema = SpreadRequest.schema()
test_schema = {k: v for k, v in SpreadRequest.schema().items()}


@given(from_schema(test_schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_spread(generated_payload):

    await _hypothesis_request(SpreadMETHOD, SpreadURL, generated_payload, KrakenFullResponse(SpreadResponse()))




#------------------------------------------------------------
# HYPOTHESIS TEST TICKER
#------------------------------------------------------------
from crypto_dom.kraken.market_data.ticker import (
        Request as TickerRequest, 
        Response as TickerResponse,
        METHOD as TickerMETHOD,
        URL as TickerURL
    )

testcases = 0
schema = TickerRequest.schema()
test_schema = {k: v for k, v in TickerRequest.schema().items()}


@given(from_schema(test_schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_ticker(generated_payload):

    await _hypothesis_request(TickerMETHOD, TickerURL, generated_payload, KrakenFullResponse(TickerResponse()))


#------------------------------------------------------------
# HYPOTHESIS TEST TRADES
#------------------------------------------------------------
from crypto_dom.kraken.market_data.trades import (
        Request as TradesRequest,
        Response as TradesResponse, 
        METHOD as TradesMETHOD, 
        URL as TradesURL
    )

testcases = 0
schema = TradesRequest.schema()
test_schema = {k: v for k, v in TradesRequest.schema().items()}


@given(from_schema(test_schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_trades(generated_payload):

    await _hypothesis_request(TradesMETHOD, TradesURL, generated_payload, KrakenFullResponse(TradesResponse()))



#------------------------------------------------------------
# HYPOTHESIS TEST ASSETPAIRS
#------------------------------------------------------------
from crypto_dom.kraken.market_data.asset_pairs import (
    Request as AssetPairsRequest,
    Response as AssetPairsResponse,
    METHOD as AssetPairsMETHOD,
    URL as AssetPairsURL
    )

testcases = 0
schema = AssetPairsRequest.schema()
test_schema = {k: v for k, v in AssetPairsRequest.schema().items()}


@given(from_schema(test_schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_assetpairs(generated_payload):

    await _hypothesis_request(AssetPairsMETHOD, AssetPairsURL, generated_payload, KrakenFullResponse(AssetPairsResponse()))



#------------------------------------------------------------
# HYPOTHESIS TEST ASSETS
#------------------------------------------------------------
from crypto_dom.kraken.market_data.assets import (
    Request as AssetsRequest,
    Response as AssetsResponse,
    METHOD as AssetsMETHOD,
    URL as AssetsURL
    )

testcases = 0
schema = AssetsRequest.schema()
test_schema = {k: v for k, v in AssetsRequest.schema().items()}


@given(from_schema(test_schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_assets(generated_payload):

    await _hypothesis_request(AssetsMETHOD, AssetsURL, generated_payload, KrakenFullResponse(AssetsResponse()))