import random
import asyncio

import stackprinter
stackprinter.set_excepthook(style="darkbg2")
import pytest
import httpx
from hypothesis import given, settings
from hypothesis_jsonschema import from_schema

from crypto_dom.result import Err, Ok
from crypto_dom.binance import BinanceFull
from crypto_dom.hypothesis_settings import DEADLINE, MAX_EXAMPLES, SUPPRESS_HEALTH_CHECK, VERBOSITY


#------------------------------------------------------------
# HYPOTHESIS BASE REQUEST
#------------------------------------------------------------

async def _hypothesis_request(method, url, generated_payload, request_model, response_model):

    async with httpx.AsyncClient() as client:

            print("Generated", generated_payload)

            # binance does not accept extra query parameters
            # hypothesis will sometimes generate random key/value pairs that dont match any model field
            # = we need to filter them out
            valid_params = request_model(**generated_payload).dict(exclude_none=True)

            print("Valid params", valid_params)

            r = await client.request(method, url, params=valid_params)
            rjson = r.json()

            # validate
            _valid = response_model(rjson)
            assert isinstance(_valid, Ok), _valid.value
            assert _valid.is_ok(), _valid.value

            assert r.status_code == 200, f"{rjson}-{r.request}"
            if hasattr(rjson, "keys"):
                assert not "code" in rjson.keys()

            await asyncio.sleep(random.randint(2, 5))




#------------------------------------------------------------
# HYPOTHESIS TEST KLINES
#------------------------------------------------------------
from crypto_dom.binance.market_data.klines import (
        Request as KlinesRequest,
        Response as KlinesResponse,
        METHOD as KlinesMETHOD,
        URL as KlinesURL
    )

schema = KlinesRequest.schema()

@given(from_schema(schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_klines(generated_payload):

    await _hypothesis_request(KlinesMETHOD, KlinesURL, generated_payload, KlinesRequest, BinanceFull(KlinesResponse()))



#------------------------------------------------------------
# HYPOTHESIS TEST ORDERBOOK
#------------------------------------------------------------
from crypto_dom.binance.market_data.orderbook_ticker import (
        Request as OBTickerRequest,
        Response as OBTickerResponse,
        METHOD as OBTickerMETHOD,
        URL as OBTickerURL
    )

schema = OBTickerRequest.schema()

@given(from_schema(schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_orderbook_ticker(generated_payload):

    await _hypothesis_request(OBTickerMETHOD, OBTickerURL, generated_payload, OBTickerRequest, BinanceFull(OBTickerResponse()))


#------------------------------------------------------------
# HYPOTHESIS TEST DEPTH
#------------------------------------------------------------
from crypto_dom.binance.market_data.depth import (
        Request as DepthRequest,
        Response as DepthResponse,
        METHOD as DepthMETHOD,
        URL as DepthURL
    )

schema = DepthRequest.schema()

@given(from_schema(schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_depth(generated_payload):

    await _hypothesis_request(DepthMETHOD, DepthURL, generated_payload, DepthRequest, BinanceFull(DepthResponse()))



#------------------------------------------------------------
# HYPOTHESIS TEST TRADES
#------------------------------------------------------------
from crypto_dom.binance.market_data.trades import (
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

    await _hypothesis_request(TradesMETHOD, TradesURL, generated_payload, TradesRequest, BinanceFull(TradesResponse()))



#------------------------------------------------------------
# HYPOTHESIS TEST AGGTRADES
#------------------------------------------------------------
from crypto_dom.binance.market_data.aggtrades import (
        Request as AggTradesRequest,
        Response as AggTradesResponse,
        METHOD as AggTradesMETHOD, 
        URL as AggTradesURL
    )

schema = AggTradesRequest.schema()

@given(from_schema(schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_aggtrades(generated_payload):

    await _hypothesis_request(AggTradesMETHOD, AggTradesURL, generated_payload, AggTradesRequest, BinanceFull(AggTradesResponse()))



#------------------------------------------------------------
# HYPOTHESIS TEST PRICE TICKER
#------------------------------------------------------------
from crypto_dom.binance.market_data.price_ticker import (
        Request as PriceTickerRequest, 
        Response as PriceTickerResponse,
        METHOD as PriceTickerMETHOD,
        URL as PriceTickerURL
    )

schema = PriceTickerRequest.schema()

@given(from_schema(schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_priceticker(generated_payload):

    await _hypothesis_request(PriceTickerMETHOD, PriceTickerURL, generated_payload, PriceTickerRequest, BinanceFull(PriceTickerResponse()))


#------------------------------------------------------------
# HYPOTHESIS TEST AVERAGE PRICE
#------------------------------------------------------------
from crypto_dom.binance.market_data.average_price import (
        Request as AvgPriceRequest,
    Response as AvgPriceResponse, 
        METHOD as AvgPriceMETHOD, 
        URL as AvgPriceURL
    )

schema = AvgPriceRequest.schema()

@given(from_schema(schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_average_price(generated_payload):

    await _hypothesis_request(AvgPriceMETHOD, AvgPriceURL, generated_payload, AvgPriceRequest, BinanceFull(AvgPriceResponse()))



#------------------------------------------------------------
# HYPOTHESIS TEST 24h TICKER
#------------------------------------------------------------
from crypto_dom.binance.market_data.daily_ticker import (
    Request as DailyTickerRequest,
    Response as DailyTickerResponse,
    METHOD as DailyTickerMETHOD,
    URL as DailyTickerURL
    )

schema = DailyTickerRequest.schema()

@given(from_schema(schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_dailyticker(generated_payload):

    await _hypothesis_request(DailyTickerMETHOD, DailyTickerURL, generated_payload, DailyTickerRequest, BinanceFull(DailyTickerResponse()))



#------------------------------------------------------------
# HYPOTHESIS TEST EXCHANGE INFO
#------------------------------------------------------------
from crypto_dom.binance.market_data.exchange_info import (
    Request as ExchInfoRequest,
    Response as ExchInfoResponse,
    METHOD as ExchInfoMETHOD,
    URL as ExchInfoURL
    )

schema = ExchInfoRequest.schema()

@given(from_schema(schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_exchangeinfo(generated_payload):

    await _hypothesis_request(ExchInfoMETHOD, ExchInfoURL, generated_payload, ExchInfoRequest, BinanceFull(ExchInfoResponse()))