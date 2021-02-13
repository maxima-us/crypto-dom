import random
import asyncio

import stackprinter
stackprinter.set_excepthook(style="darkbg2")
import pytest
import httpx
import pydantic
from hypothesis import given, settings
from hypothesis_jsonschema import from_schema

from crypto_dom.result import Err, Ok

from crypto_dom.kraken import KrakenFullResponse
from crypto_dom.hypothesis_settings import DEADLINE, MAX_EXAMPLES, SUPPRESS_HEALTH_CHECK, VERBOSITY




#------------------------------------------------------------
# HYPOTHESIS BASE REQUEST
#------------------------------------------------------------

async def _hypothesis_request(method, url, generated_payload, response_model):

    async with httpx.AsyncClient() as client:

            print("Generated", generated_payload)

            r = await client.request(method, url, params=generated_payload)
            rjson = r.json()

            # validate
            _valid = response_model(rjson)
            assert isinstance(_valid, Ok), _valid.value
            assert _valid.is_ok(), _valid.value

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

@given(from_schema(schema))
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

@given(from_schema(schema))
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

@given(from_schema(schema))
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

@given(from_schema(schema))
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

schema = TickerRequest.schema()

@given(from_schema(schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_ticker(generated_payload):

    await _hypothesis_request(TickerMETHOD, TickerURL, generated_payload, KrakenFullResponse(TickerResponse()))



#------------------------------------------------------------
# HYPOTHESIS TEST ASSETPAIRS
#------------------------------------------------------------
from crypto_dom.kraken.market_data.asset_pairs import (
    Request as AssetPairsRequest,
    Response as AssetPairsResponse,
    METHOD as AssetPairsMETHOD,
    URL as AssetPairsURL
    )

schema = AssetPairsRequest.schema()

@given(from_schema(schema))
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

schema = AssetsRequest.schema()

@given(from_schema(schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_assets(generated_payload):

    await _hypothesis_request(AssetsMETHOD, AssetsURL, generated_payload, KrakenFullResponse(AssetsResponse()))