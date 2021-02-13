import random
import asyncio
import time

import stackprinter
stackprinter.set_excepthook(style="darkbg2")
import pytest
import httpx
from hypothesis import given, settings
from hypothesis_jsonschema import from_schema

from crypto_dom.result import Err, Ok
from crypto_dom.kraken import KrakenFullResponse
from crypto_dom.kraken.__sign import get_keys, EmptyEnv, auth_headers
from crypto_dom.hypothesis_settings import DEADLINE, MAX_EXAMPLES, SUPPRESS_HEALTH_CHECK, VERBOSITY


def make_nonce():
    return int(time.time()*10**3)


#------------------------------------------------------------
# HYPOTHESIS BASE REQUEST
#------------------------------------------------------------


async def _hypothesis_request(method, url, generated_payload, request_model, response_model):


    async with httpx.AsyncClient() as client:

            try:
                keyset = get_keys() # returns a set of tuples (key, secret)
            except EmptyEnv:
                # do not proceed to send a test request in this case
                return
            key, secret = keyset.pop()
            del generated_payload["nonce"]
            generated_payload["nonce"] = make_nonce()

            valid_payload = request_model(**generated_payload).dict(exclude_none=True)
            print("Valid", valid_payload)

            headers = auth_headers(url, valid_payload, key=key, secret=secret)

            # kraken private endpoints are always post requests
            r = await client.request(method, url, data=valid_payload, headers=headers)
            rjson = r.json()

            # validate
            _valid = response_model(rjson)
            assert isinstance(_valid, Ok), _valid.value
            assert _valid.is_ok(), _valid.value

            assert r.status_code == 200, rjson
            assert rjson["error"] == [], r.request

            await asyncio.sleep(random.randint(2, 5))



#------------------------------------------------------------
# HYPOTHESIS TEST CLOSED ORDERS
#------------------------------------------------------------
from crypto_dom.kraken.user_data.closed_orders import (
        Request as ClORequest,
        Response as ClOResponse,
        METHOD as ClOMETHOD,
        URL as ClOURL
    )

schema = ClORequest.schema()

@given(from_schema(schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_closedorders(generated_payload):
    
    await _hypothesis_request(ClOMETHOD, ClOURL, generated_payload, ClORequest, KrakenFullResponse(ClOResponse()))



#------------------------------------------------------------
# HYPOTHESIS TEST OPEN ORDERS
#------------------------------------------------------------
from crypto_dom.kraken.user_data.open_orders import (
        Request as OpORequest,
        Response as OpOResponse,
        METHOD as OpOMETHOD,
        URL as OpOURL
    )

schema = OpORequest.schema()

@given(from_schema(schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_openorders(generated_payload):
    
    await _hypothesis_request(OpOMETHOD, OpOURL, generated_payload, OpORequest, KrakenFullResponse(OpOResponse()))