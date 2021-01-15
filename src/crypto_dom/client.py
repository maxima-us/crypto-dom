
import asyncio

import httpx
from pydantic import ValidationError
from returns.io import IOFailure, IOSuccess

from crypto_dom.kraken.ohlc import _OhlcReq, _OhlcResp, URL, METHOD


#================================================================================
# SUBCLASS HTTPX.ASYNCLIENT 
#================================================================================


class UnsetType:
    pass  # pragma: nocover


UNSET = UnsetType()




class HttypeClient(httpx.AsyncClient):

    async def safe_request(
        self,
        method,
        url,
        *,
        t_in= None,
        t_out= None,
        content=None,
        data=None,
        files=None,
        json=None,
        params = None,
        headers= None,
        cookies= None,
        auth= None,
        allow_redirects: bool = True,
        timeout = None
        ):

        # From: 
        # https://www.python-httpx.org/compatibility/
        # The HTTP GET, DELETE, HEAD, and OPTIONS methods are specified as not supporting a request body. 
        # To stay in line with this, the .get, .delete, .head and .options functions do not support files, data, or json arguments.

        # See also: 
        # https://specs.openstack.org/openstack/api-wg/guidelines/http/methods.html#http-methods

        _new_params = params
        _new_data = data

        if t_in:

            if params:
                # for methods: GET, DELETE, HEAD, OPTIONS
                # validate query params
                try:
                    valid_req = t_in(**params)
                    _new_params = valid_req.dict(exclude_none=True)
                except ValidationError as e:
                    return IOFailure(e)
                except Exception as e:
                    return IOFailure(e)
            if data:
                # for methods: POST, PUT, PATCH
                # valid request body
                try:
                    valid_req = t_in(**data)
                    _new_data = valid_req.dict(exclude_none=True)
                except ValidationError as e:
                    return IOFailure(e)
                except Exception as e:
                    return IOFailure(e)
            
        try:
            r = await self.request(
                method,
                url,
                content=content,
                data=_new_data,
                files=files,
                json=json,
                params = _new_params,
                headers= headers,
                cookies= cookies,
                auth= auth,
                allow_redirects = allow_redirects,
                timeout=timeout
            )
        except Exception as e:
            return IOFailure(e)

        rjson = r.json()
        _new_content = rjson

        if t_out:
            try:
                # TODO this is specific to kraken (the result key)
                result = rjson["result"]
                valid_resp = t_out(**result)
                print("Valid Resp", type(valid_resp))
                _new_content = IOSuccess(valid_resp)
                print("Updated content", type(_new_content))
                print("Updated content inner value", type(_new_content._inner_value))
                print("Updated content inner value **2", type(_new_content._inner_value._inner_value))
            except ValidationError as e:
                return IOFailure(e)
            except Exception as e:
                return IOFailure(e)


        # add a new attribute to the response object 
        setattr(r, "safe_content", _new_content)

        return IOSuccess(r)


client = HttypeClient()
payload = {
    "pair": "XXBTZUSD",
    "interval": 60
}


async def ohlc():
    r = await client.safe_request(METHOD, URL, t_in=_OhlcReq, t_out=_OhlcResp("XXBTZUSD"), params=payload)
    # r = await client.request(METHOD, URL, params=payload)
    return r

ohlc = asyncio.run(ohlc())
print(ohlc)
# print(ohlc.unwrap())


def show(result):
    print(result)
    return result

print("Response type", type(ohlc))
ohlc.apply(show)