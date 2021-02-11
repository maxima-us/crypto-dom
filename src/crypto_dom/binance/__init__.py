import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.result import Err, Ok



class ErrorResponse(pydantic.BaseModel):
    """Error Model for API and SAPI endpoints

    Note:
    -----
        Different for WAPI !!!
    """

    code: int
    msg: str



class BinanceFull:

    def __init__(self, success_model):
        self.success_model = success_model

    def __call__(self, full_response: dict):
        
        # check if response is a dict
        # if its a list we know for sure it was not an error
        if hasattr(full_response, "keys"):
            # check if response is an error
            if "code" in full_response.keys():
                if full_response["msg"]:
                    try:
                        _err = ErrorResponse(**full_response)
                        return Err(_err)

                    except pydantic.ValidationError as e:
                        return Err(e)

                else:
                    return Err(f"No error message : {full_response}") 


        else:
            try:
                # check if it is a pydantic model
                if hasattr(self.success_model, "__fields__"):
                    _res = self.success_model(**full_response)
                    return Ok(_res)

                # else its a wrapper around pydantic that we defined 
                else: 
                    _res = self.success_model(full_response)
                    return Ok(_res)
                
            except pydantic.ValidationError as e:
                return Err(e)
    