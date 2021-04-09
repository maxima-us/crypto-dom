

import pydantic

from crypto_dom.result import Err, Ok


class ErrorResponse(pydantic.BaseModel):

    code: int
    msg: str
    success: bool



class BybtFull:

    def __init__(self, success_model):
        self.success_model = success_model

    def __call__(self, full_response: dict):

        if hasattr(full_response, "keys"):

            # check if response is an error
            if "success" in full_response.keys():
                if not full_response["success"]:
                    try:
                        _err = ErrorResponse(**full_response)
                        return Err(_err)
                    except pydantic.ValidationError as e:
                        return Err(e)


            if "data" in full_response.keys():                

                data = full_response["data"]
                
                # check if it is a pydantic model
                if hasattr(self.success_model, "__fields__"):
                    try:
                        _res = self.success_model(**data)
                        return Ok(_res)
                    except pydantic.ValidationError as e:
                        return Err(e)

                else:
                    try:
                        _res = self.success_model(data)
                        return Ok(_res)
                    except pydantic.ValidationError as e:
                        return Err(e)
                

