import asyncio
import time
from typing import Optional, Mapping, Any, Iterable, Awaitable, Callable, Union
import functools

import httpx
import aiohttp
from pydantic import ValidationError


from crypto_dom.result import Result, Ok, Err

from crypto_dom.kraken.__sign import get_keys, auth_headers



#================================================================================
# SUBCLASS HTTPX.ASYNCLIENT 
#================================================================================


# TODO type the client args (see httpx repo)


class _TypedHttpxClient(httpx.AsyncClient):

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
        headers = None,
        auth_headers: Optional[Callable] = None,
        cookies= None,
        auth= None,
        allow_redirects: bool = True,
        timeout = None
        ) -> Result:

        # From: 
        # https://www.python-httpx.org/compatibility/
        # The HTTP GET, DELETE, HEAD, and OPTIONS methods are specified as not supporting a request body. 
        # To stay in line with this, the .get, .delete, .head and .options functions do not support files, data, or json arguments.

        # See also: 
        # https://specs.openstack.org/openstack/api-wg/guidelines/http/methods.html#http-methods

       
        _new_params = params
        _new_data = data
        _new_headers = None

        if t_in:

            if params:
                # for methods: GET, DELETE, HEAD, OPTIONS
                # validate query params
                try:
                    valid_req = t_in(**params)
                    _new_params = valid_req.dict(exclude_none=True)

                    # ! falsify (for testing)
                    # _new_params["pair"] = "XXBTUEE"
                    
                except ValidationError as e:
                    return Err(e)
                except Exception as e:
                    return Err(e)
            if data:
                # for methods: POST, PUT, PATCH
                # valid request body
                try:
                    valid_req = t_in(**data)
                    _new_data = valid_req.dict(exclude_none=True)
                    
                    # print("\nNew post data", _new_data)     # debugging

                    # BELOW IS FOR DEBUGGING
                    # TODO: auth headers need to use `_new_data`, not `data`
                    # ! BUT: hashing will change from one exchange to another, and input param to hashing/generating the signature will too
                    # ? pass partial function, only param that is always there is `data` (payload dict)
                    # keyset = get_keys()
                    # key, secret = keyset.pop()
                    # _new_headers = auth_headers(url, _new_data, key=key, secret=secret)
                    # print("\nNew hears", _new_headers)

                    _new_headers = auth_headers(url=url, data=_new_data)

                except ValidationError as e:
                    return Err(e)
                except Exception as e:
                    raise Err(e)
            
        try:
            r = await self.request(
                method,
                url,
                content=content,
                data=_new_data,
                files=files,
                json=json,
                params=_new_params,
                headers=_new_headers if _new_headers else headers,
                cookies=cookies,
                auth=auth,
                allow_redirects=allow_redirects,
                timeout=timeout
            )
        except Exception as e:
            return Err(e)

        rjson = r.json()

        #! falsify (for testing)
        # rjson["result"]["last"] = "random string"

        _new_content = rjson

        if t_out:
            try:
                # # TODO this is specific to kraken (the result key)
                # # print(rjson)
                # if not rjson.get("error"):
                #     result = rjson["result"]
                #     valid_resp = t_out(result)  # TODO verify after model syntax update
                #     # print("Valid Resp", type(valid_resp))
                #     # TODO should this be wrapped in a Result ???
                #     _new_content = valid_resp
                #     # print("Updated content", type(_new_content))
                #     # print("Updated content inner value", type(_new_content._inner_value))
                #     # print("Updated content inner value **2", type(_new_content._inner_value._inner_value))
                # else:
                #     _new_content = rjson["error"]

                #! general case
                _new_content: Result = t_out(rjson)


                # cryptodom's full response models return ValidatioNError wrapped in Err
                # so it wont be caught by try/except block => instance check
                # if isinstance(_new_content.value, ValidationError):
                #     # already wrapped in Err
                #     return _new_content

            except ValidationError as e:
                return Err(e)
            except Exception as e:
                return Err(e)


        # add a new attribute to the response object 
        setattr(r, "safe_content", _new_content)

        return Ok(r)




#================================================================================
# SUBCLASS AIOHTTP.CLIENTSESSION
#================================================================================

class _TypedAioHttpClient(aiohttp.ClientSession):

    from typing import NewType
    from types import SimpleNamespace
    from ssl import SSLContext
    from aiohttp.typedefs import LooseCookies, LooseHeaders, StrOrURL
    from aiohttp.client_reqrep import Fingerprint, ClientResponse
    from aiohttp.helpers import BasicAuth, sentinel
    from aiohttp.client import ClientTimeout

    _SENTINEL = NewType("_SENTINEL", object)


    # see: https://github.com/aio-libs/aiohttp/blob/3250c5d75a54e19e2825d0a609f9d9cd4bf62087/aiohttp/client.py#L306
    async def safe_request(
        self,
        method: str,
        str_or_url: StrOrURL,
        *,
        t_in= None,
        t_out= None,
        params: Optional[Mapping[str, str]] = None,
        data: Any = None,
        json: Any = None,
        cookies: Optional[LooseCookies] = None,
        headers: Optional[LooseHeaders] = None,
        auth_headers: Optional[Callable] = None,
        skip_auto_headers: Optional[Iterable[str]] = None,
        auth: Optional[BasicAuth] = None,
        allow_redirects: bool = True,
        max_redirects: int = 10,
        compress: Optional[str] = None,
        chunked: Optional[bool] = None,
        expect100: bool = False,
        raise_for_status: Union[
            None, bool, Callable[[ClientResponse], Awaitable[None]]
        ] = None,
        read_until_eof: bool = True,
        proxy: Optional[StrOrURL] = None,
        proxy_auth: Optional[BasicAuth] = None,
        timeout: Union[ClientTimeout, _SENTINEL] = sentinel,
        ssl: Optional[Union[SSLContext, bool, Fingerprint]] = None,
        proxy_headers: Optional[LooseHeaders] = None,
        trace_request_ctx: Optional[SimpleNamespace] = None,
        read_bufsize: Optional[int] = None,
    ):

        _new_params = params
        _new_data = data
        _new_headers = None

        if t_in:

            if params:
                # for methods: GET, DELETE, HEAD, OPTIONS
                # validate query params
                try:
                    valid_req = t_in(**params)  # TODO verify after model syntax update
                    _new_params = valid_req.dict(exclude_none=True)
                except ValidationError as e:
                    return Err(e)
                except Exception as e:
                    return Err(e)
            if data:
                # for methods: POST, PUT, PATCH
                # valid request body
                try:
                    valid_req = t_in(**data)    # TODO verify after model syntax update
                    _new_data = valid_req.dict(exclude_none=True)
                    _new_headers = auth_headers(url=str_or_url, data=_new_data)
                except ValidationError as e:
                    return Err(e)
                except Exception as e:
                    return Err(e)

            # TODO do we have to handle json kwarg as well ???

        try:
            r = await self.request(
                method,
                str_or_url,
                params=_new_params, 
                data=_new_data,
                json=json,
                cookies=cookies,
                headers=_new_headers if _new_headers else headers,
                skip_auto_headers=skip_auto_headers,
                auth=auth,
                allow_redirects=allow_redirects,
                max_redirects=max_redirects,
                compress=compress,
                chunked=chunked,
                expect100=expect100,
                raise_for_status=raise_for_status,
                read_until_eof=read_until_eof,
                proxy=proxy,
                proxy_auth=proxy_auth,
                timeout=timeout,
                ssl=ssl,
                proxy_headers=proxy_headers,
                trace_request_ctx=trace_request_ctx,
                read_bufsize=read_bufsize
                
            )
        except Exception as e:
            return Err(e)

        # see: https://github.com/aio-libs/aiohttp/blob/3250c5d75a54e19e2825d0a609f9d9cd4bf62087/aiohttp/client_reqrep.py#L1016
        rjson = await r.json()
        _new_content = rjson

        if t_out:
            try:
                # # TODO this is specific to kraken (the result key)
                # result = rjson["result"]
                # valid_resp = t_out(result)  # TODO verify after model syntax update
                # # print("Valid Resp", type(valid_resp))
                # # TODO should this be wrapped in a Result ???
                # _new_content = valid_resp
                
                # Update
                _new_content = t_out(rjson)

            except ValidationError as e:
                return Err(e)
            except Exception as e:
                return Err(e)

        # add a new attribute to the ClientResponse object
        # see: https://github.com/aio-libs/aiohttp/blob/3250c5d75a54e19e2825d0a609f9d9cd4bf62087/aiohttp/client_reqrep.py#L648
        setattr(r, "safe_content", _new_content)
        
        return Ok(r)

#================================================================================
# INTERFACE
#================================================================================


class HttypeClient:

    number = 1
    httpx = _TypedHttpxClient
    aiohttp = _TypedAioHttpClient


#================================================================================
# RUN 
#================================================================================


if __name__ == "__main__":
    from crypto_dom.kraken.market_data.ohlc import Request, Response, URL, METHOD
    from crypto_dom.kraken.user_trading.add_order import METHOD as NO_METH, URL as NO_URL, Request as NO_Req, Response as NO_Resp, _AddOrderResponse
    from crypto_dom.kraken import KrakenFullResponse

    # ----- OHLC 
    
    payload = {
        "pair": "XXBTZUSD",
        "interval": 60
    }

    async def ohlc(client):
        async with client:
            #! update client to now take in Full Response model (including error)
            r = await client.safe_request(METHOD, URL, t_in=Request, t_out=KrakenFullResponse(Response()), params=payload)
        
        # ! also works if we do not provide models (but will still return value wrapped in Result)
        # r = await client.request(METHOD, URL, params=payload)
        
        return r


    # ----- NEW ORDER
    

    def make_nonce():
        return int(time.time()*10**3)

    order_data = {
        "pair": "XZECZUSD",
        "type": "sell",
        "ordertype": "limit",
        "price": 100,
        "volume": 1,
        "nonce": make_nonce()
    }

    keyset = get_keys()
    key, secret = keyset.pop()
    headers = auth_headers(NO_URL, order_data, key=key, secret=secret)

    kraken_auth_headers = functools.partial(auth_headers, NO_URL, key=key, secret=secret)


    async def new_order(client):
        async with client:
            #! update client to now take in Full Response model (including error)
            #! auth_headers is a function
            r = await client.safe_request(NO_METH, NO_URL, t_in=NO_Req, t_out=KrakenFullResponse(NO_Resp()), data=order_data, auth_headers=kraken_auth_headers)
            return r


    # --------------------
    # HTTPX
    # --------------------
    
    # ! httpx Client can be instantiated anywhere
    httpx_client = _TypedHttpxClient()

    # ----- OHLC 
    candles = asyncio.run(ohlc(httpx_client))
    
    if candles.is_ok():
        print("Safe content", candles.value.safe_content)
        print("JSON content", candles.value.json())
    else:
        print(candles.value)

    # ----- NEW ORDER
    order = asyncio.run(new_order(httpx_client))
    
    if order.is_ok():
        print("Safe content", order.value.safe_content)
        print("JSON content", order.value.json())
    else:
        print(order.value)



    # --------------------
    # AIOHTTP
    # --------------------

    # ! aiohttp session NEEDS to be instantiated inside a coroutine
    #   see: https://stackoverflow.com/a/55186375
    async def aiohttp_req():
        client = _TypedAioHttpClient()
        return await ohlc(client)

    # result = asyncio.run(aiohttp_req()) 
    # print("\naiohttp response", result)
    # print("\naiohttp response type", tye(result))
