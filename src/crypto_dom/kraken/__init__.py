import typing

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.result import Err, Ok, Result



class ErrorResponse(pydantic.BaseModel):

    error: typing.Tuple[typing.Optional[str], ...]


class KrakenFullResponse:

    def __init__(self, success_model):
        self.success_model = success_model

    def __call__(self, full_response: dict) -> Result[pydantic.BaseModel, Exception]:

        # check is response is an error
        if not "result" in full_response.keys():
            if full_response.get("error"):
                try:
                    _err = ErrorResponse(**full_response)
                    return Err(_err)
                except pydantic.ValidationError as e:
                    return Err(e)
            else:
                return Err(f"{full_response}")


        else:
            try:
                # check if its a pydantic model
                if hasattr(self.success_model, "__fields__"):
                    try:
                        _res = self.success_model(**full_response["result"])
                        return Ok(_res)
                    except pydantic.ValidationError as e:
                        return Err(e)
                # its a wrapper around pydantic that we defined
                else:
                    try:
                        _res = self.success_model(full_response["result"])
                        return Ok(_res)
                    except pydantic.ValidationError as e:
                        return Err(e)
                
            except pydantic.ValidationError as e:
                return Err(e)



if __name__ == "__main__":

    import asyncio
    import httpx

    from crypto_dom.kraken.market_data.trades import Request, URL, METHOD
    from crypto_dom.kraken.market_data.ohlc import Response


    payload = {
        "pair": "XXBTZUSD",
        "interval": 60
    }


    async def test():

        async with httpx.AsyncClient() as client:
            r = await client.request(METHOD, URL, params=payload)
            rjson = r.json()

            try: 
                _model = KrakenFullResponse(Response())
                _valid = _model(rjson)
                print(_valid)
            except pydantic.ValidationError as e:
                print(e)

    asyncio.run(test())