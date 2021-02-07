
import random
import asyncio

import pytest
import httpx

from hypothesis import given, settings
from hypothesis_jsonschema import from_schema

from crypto_dom.kraken import KrakenFullResponse
from crypto_dom.kraken.market_data.orderbook import Request, Response, METHOD, URL

from crypto_dom.hypothesis_settings import DEADLINE, MAX_EXAMPLES, SUPPRESS_HEALTH_CHECK, VERBOSITY


#------------------------------------------------------------
# FIXME max_examples argument doesnt seem to work
#------------------------------------------------------------

testcases = 0

schema = Request.schema()
test_schema = {k: v for k, v in Request.schema().items()}


@given(from_schema(test_schema))
@settings(deadline=DEADLINE, max_examples=MAX_EXAMPLES, suppress_health_check=SUPPRESS_HEALTH_CHECK, verbosity=VERBOSITY)
@pytest.mark.asyncio
async def test_gen_request_orderbook(generated_payload):

    async with httpx.AsyncClient() as client:
        global testcases
        testcases += 1
        
        if testcases > 5:
            assert True
        
        print("Tested Cases", testcases)
        print("Generated", generated_payload)

        r = await client.request(METHOD, URL, params=generated_payload)
        rjson = r.json()

        expected_full = KrakenFullResponse(Response())
        
        # validate
        expected_full(rjson)

        assert r.status_code == 200, len(rjson[generated_payload["pair"]])
        assert rjson["error"] == []

        await asyncio.sleep(random.randint(2, 5))


