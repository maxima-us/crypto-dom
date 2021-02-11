import random
import asyncio

import stackprinter
stackprinter.set_excepthook(style="darkbg2")
import pytest
import httpx
from hypothesis import given, settings, strategies as st
from hypothesis_jsonschema import from_schema

from crypto_dom.binance import BinanceFull
from crypto_dom.binance.__sign import (
    get_keys as b_get_keys, 
    auth_headers as b_auth_headers,
    auth_payload,
    auth_timestamp,
    EmptyEnv
)

from crypto_dom.binance.definitions import ORDER_RESP_TYPE, SYMBOL, ORDER_SIDE, ORDER_TIF, ORDER_TYPE
from crypto_dom.hypothesis_settings import DEADLINE, MAX_EXAMPLES, SUPPRESS_HEALTH_CHECK, VERBOSITY




#------------------------------------------------------------
# HYPOTHESIS BASE REQUEST
#------------------------------------------------------------

async def _hypothesis_request(method, url, generated_payload, request_model, response_model):

    testcases = 0
    async with httpx.AsyncClient() as client:
        # global testcases
        testcases += 1

        if testcases > 5:
            print("Skipping Test Case")
            assert True

        print("Tested Cases", testcases)
        print("Generated", generated_payload)

        # binance does not accept extra query parameters
        # hypothesis will sometimes generate random key/value pairs that dont match any model field
        # = we need to filter them out
        generated_payload["timestamp"] = auth_timestamp()
        valid_params = request_model(**generated_payload).dict(exclude_none=True)

        print("Valid params", valid_params)

        # get keys from env
        try:
            keyset = b_get_keys()
        except EmptyEnv as e:
            raise e
            
        # auth
        key, secret = keyset.pop()
        headers = b_auth_headers(key=key)
        signed_payload = auth_payload(url, valid_params, secret=secret)
        
        # send req
        if method in ["POST"]:
            # data has to be a dict, cant accept list of tuples
            if isinstance(signed_payload, list):
                signed_payload = dict(signed_payload)
                print("Signed payload", signed_payload)
            r = await client.request(method, url, data=signed_payload, headers=headers)
        else:
            r = await client.request(method, url, params=signed_payload, headers=headers)

        rjson = r.json()

        # validate
        response_model(rjson)

        if hasattr(rjson, "keys"):
            # its an error
            if "code" in rjson.keys():
                # we accept filter failures, since
                # we cant really generate test cases that will pass that
                assert rjson["code"] == -1013, f"{rjson}-{r.request}"
            
            # its a valid dict response
            else:
                assert r.status_code == 200, f"{rjson}-{r.request}"

        # response is a list
        else:
            assert r.status_code == 200, f"{rjson}-{r.request}"
            

        await asyncio.sleep(random.randint(2, 5))



#------------------------------------------------------------
# HYPOTHESIS TEST ACCOUNT INFORMATION (USER DATA)
#------------------------------------------------------------
from crypto_dom.binance.spot_account.account_information import (
        Request as AccountInfoRequest,
        Response as AccountInfoResponse,
        METHOD as AccountInfoMETHOD,
        URL as AccountInfoURL
    )

schema = AccountInfoRequest.schema()

@given(from_schema(schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_accountinfo(generated_payload):

    await _hypothesis_request(AccountInfoMETHOD, AccountInfoURL, generated_payload, AccountInfoRequest, BinanceFull(AccountInfoResponse()))



#------------------------------------------------------------
# HYPOTHESIS TEST ACCOUNT TRADE LIST (USER DATA)
#------------------------------------------------------------
from crypto_dom.binance.spot_account.account_trade_list import (
        Request as AccountTradeListRequest,
        Response as AccountTradeListResponse,
        METHOD as AccountTradeListMETHOD,
        URL as AccountTradeListURL
    )

schema = AccountTradeListRequest.schema()

@given(from_schema(schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_accounttradelist(generated_payload):

    await _hypothesis_request(AccountTradeListMETHOD, AccountTradeListURL, generated_payload, AccountTradeListRequest, BinanceFull(AccountTradeListResponse()))


#------------------------------------------------------------
# HYPOTHESIS TEST ALL ORDERS (USER DATA) 
#------------------------------------------------------------
from crypto_dom.binance.spot_account.all_orders import (
        Request as AllOrdersRequest,
        Response as AllOrdersResponse,
        METHOD as AllOrdersMETHOD,
        URL as AllOrdersURL
    )

schema = AllOrdersRequest.schema()

@given(from_schema(schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_allorders(generated_payload):

    await _hypothesis_request(AllOrdersMETHOD, AllOrdersURL, generated_payload, AllOrdersRequest, BinanceFull(AllOrdersResponse()))


#------------------------------------------------------------
# HYPOTHESIS TEST OPEN ORDERS (USER DATA) 
#------------------------------------------------------------
from crypto_dom.binance.spot_account.open_orders import (
        Request as OpenOrdersRequest,
        Response as OpenOrdersResponse,
        METHOD as OpenOrdersMETHOD,
        URL as OpenOrdersURL
    )

schema = OpenOrdersRequest.schema()

@given(from_schema(schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_openorders(generated_payload):

    await _hypothesis_request(OpenOrdersMETHOD, OpenOrdersURL, generated_payload, OpenOrdersRequest, BinanceFull(OpenOrdersResponse()))
    
        
#------------------------------------------------------------
# HYPOTHESIS TEST ALL OCO (USER DATA) 
# TODO hypothesis strat needs to be custom since we have validators for request (conditional params)
# ! we cant pass in fromId anyway, so might as well always pass in start and end times
#------------------------------------------------------------
from crypto_dom.binance.spot_account.query_all_oco import (
        Request as AllOCORequest,
        Response as AllOCOResponse,
        METHOD as AllOCOMETHOD,
        URL as AllOCOURL
    )

schema = AllOCORequest.schema()


@given(from_schema(schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def skip_gen_request_alloco(generated_payload):   # ! skipping until fixed

    await _hypothesis_request(AllOCOMETHOD, AllOCOURL, generated_payload, AllOCORequest, BinanceFull(AllOCOResponse()))



#------------------------------------------------------------
# HYPOTHESIS TEST NEW ORDER (TEST) (USER TRADING) 
# TODO hypothesis strat needs to be custom since we have validators for request (conditional params)
# ! see: https://stackoverflow.com/a/61814562
#------------------------------------------------------------
from crypto_dom.binance.spot_account.test_new_order import (
        Request as TestNewORequest,
        Response as TestNewOResponse,
        METHOD as TestNewOMETHOD,
        URL as TestNewOURL
    )

schema = TestNewORequest.schema()


@st.composite
def generate_symbol(draw):
    return draw(st.sampled_from(SYMBOL.__args__))

@st.composite
def generate_side(draw):
    return draw(st.sampled_from(ORDER_SIDE.__args__))

@st.composite
def generate_ordertype(draw):
    return draw(st.sampled_from(ORDER_TYPE.__args__))

@st.composite
def generate_resptype(draw):
    return draw(st.sampled_from(ORDER_RESP_TYPE.__args__))


# ---- Conditionals

@st.composite
def generate_quantity(draw):
    return draw(st.decimals(min_value=10, max_value=20, places=2))

@st.composite
def generate_price(draw):
    return draw(st.decimals(min_value=10, max_value=50_000, places=2))

@st.composite
def generate_tif(draw):
    return draw(st.sampled_from(ORDER_TIF.__args__))


@st.composite
def generate_test_order(draw):
    order = {
        "symbol": draw(generate_symbol()),
        "side": draw(generate_side()),
        "timestamp": auth_timestamp(),
        "newOrderRespType": draw(generate_resptype()),
        "type": draw(generate_ordertype()),
    }

    if order["type"] == "MARKET":
        # TODO how to tell we want either one key or another but not both
        order["quantity"] = draw(generate_quantity())

    if order["type"] == "LIMIT":
        order["timeInForce"] = draw(generate_tif())
        order["price"] = draw(generate_price())
        order["quantity"] = draw(generate_quantity())
    
    if order["type"] in ["STOP_LOSS", "TAKE_PROFIT"]:
        order["quantity"] = draw(generate_quantity())
        order["stopPrice"] = draw(generate_price())
    
    if order["type"] in ["STOP_LOSS_LIMIT", "TAKE_PROFIT_LIMIT"]:
        order["quantity"] = draw(generate_quantity())
        order["stopPrice"] = draw(generate_price())
        order["timeInForce"] = draw(generate_tif())
        order["price"] = draw(generate_price())

    if order["type"] in ["LIMIT_MAKER"]:
        order["quantity"] = draw(generate_quantity())
        order["price"] = draw(generate_price())

    return order


@given(generated_payload=generate_test_order())
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_testneworder(generated_payload):

    await _hypothesis_request(TestNewOMETHOD, TestNewOURL, generated_payload, TestNewORequest, BinanceFull(TestNewOResponse()))