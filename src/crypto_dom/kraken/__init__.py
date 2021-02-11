import typing

import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.result import Err, Ok



class ErrorResponse(pydantic.BaseModel):

    error: typing.Tuple[typing.Optional[str], ...]


class KrakenFullResponse:

    def __init__(self, success_model):
        self.success_model = success_model

    def __call__(self, full_response: dict):

        # check is response is an error
        if not "result" in full_response.keys():
            if full_response["error"]:
                try:
                    _err = ErrorResponse(**full_response)
                    return Err(_err)
                except pydantic.ValidationError as e:
                    return Err(e)
            else:
                return Err(f"Empty Response : {full_response}")


        else:
            try:
                # check if its a pydantic model
                if hasattr(self.success_model, "__fields__"):
                    _res = self.success_model(**full_response["result"])
                    return Ok(_res)

                # its a wrapper around pydantic that we defined
                else:
                    _res = self.success_model(full_response["result"])
                    return Ok(_res)
                
            except pydantic.ValidationError as e:
                return Err(e)