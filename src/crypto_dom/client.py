import asyncio
from typing import Optional, Mapping, Any, Iterable, Awaitable, Callable, Union
from aiohttp.payload import register_payload

import httpx
import aiohttp
from pydantic import ValidationError
from returns.io import IOFailure, IOSuccess

from crypto_dom.kraken.ohlc import _OhlcReq, _OhlcResp, URL, METHOD




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
                # print("Valid Resp", type(valid_resp))
                # TODO should this be wrapped in a Result ???
                _new_content = IOSuccess(valid_resp)
                # print("Updated content", type(_new_content))
                # print("Updated content inner value", type(_new_content._inner_value))
                # print("Updated content inner value **2", type(_new_content._inner_value._inner_value))
            except ValidationError as e:
                return IOFailure(e)
            except Exception as e:
                return IOFailure(e)


        # add a new attribute to the response object 
        setattr(r, "safe_content", _new_content)

        return IOSuccess(r)




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

            # TODO do we have to handle json kwarg as well ???

        try:
            r = await self.request(
                method,
                str_or_url,
                params=_new_params, 
                data=_new_data,
                json=json,
                cookies=cookies,
                headers=headers,
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
            return IOFailure(e)

        # see: https://github.com/aio-libs/aiohttp/blob/3250c5d75a54e19e2825d0a609f9d9cd4bf62087/aiohttp/client_reqrep.py#L1016
        rjson = await r.json()
        _new_content = rjson

        if t_out:
            try:
                # TODO this is specific to kraken (the result key)
                result = rjson["result"]
                valid_resp = t_out(**result)
                # print("Valid Resp", type(valid_resp))
                # TODO should this be wrapped in a Result ???
                _new_content = IOSuccess(valid_resp)
            except ValidationError as e:
                return IOFailure(e)
            except Exception as e:
                return IOFailure(e)

        # add a new attribute to the ClientResponse object
        # see: https://github.com/aio-libs/aiohttp/blob/3250c5d75a54e19e2825d0a609f9d9cd4bf62087/aiohttp/client_reqrep.py#L648
        setattr(r, "safe_content", _new_content)
        
        return IOSuccess(r)

#================================================================================
# INTERFACE
#================================================================================







#================================================================================
# RUN 
#================================================================================


if __name__ == "__main__":


    # ! httpx Client can be instantiated anywhere
    httpx_client = _TypedHttpxClient()
    
    payload = {
        "pair": "XXBTZUSD",
        "interval": 60
    }

    async def ohlc(client):
        async with client:
            r = await client.safe_request(METHOD, URL, t_in=_OhlcReq, t_out=_OhlcResp("XXBTZUSD"), params=payload)
        
        # ! also works if we do not provide models (but will return value wrapped in Result)
        # r = await client.request(METHOD, URL, params=payload)
        
        return r

    result= asyncio.run(ohlc(httpx_client))
    print("httpx response", result)
    print("httpx response type", type(result))

    # ! aiohttp session NEEDS to be instantiated inside a coroutine
    #   see: https://stackoverflow.com/a/55186375
    async def aiohttp_req():
        client = _TypedAioHttpClient()
        return await ohlc(client)

    result = asyncio.run(aiohttp_req()) 
    print("aiohttp response", result)
    print("aiohttp response type", type(result))
