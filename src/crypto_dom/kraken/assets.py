import typing
from datetime import date
from decimal import Decimal

from typing_extensions import Literal
import pydantic
import stackprinter
stackprinter.set_excepthook(style="darkbg2")

from crypto_dom.kraken.definitions import ASSET


# ============================================================
# ASSETS
# ============================================================


# doc: https://www.kraken.com/features/api#get-asset-info

URL = "https://api.kraken.com/0/public/Assets"
METHOD = "GET"


# ------------------------------
# Sample Response
# ------------------------------


#     {
#         "error": [],
#         "result": {
#             "ADA": {"aclass": "currency", "altname": "ADA", "decimals": 8, "display_decimals": 6},
#             "BCH": {"aclass": "currency", "altname": "BCH", "decimals": 10, "display_decimals": 5},
#             ...
#         },
#     }


# ------------------------------
# Request Model
# ------------------------------


class AssetsReq(pydantic.BaseModel):
    """Request Model for endpoint https://api.kraken.com/0/public/Assets

    Model Fields:
    -------
        info: str
            info to retrieve (optional):
                info = all info (default)
        aclass : str
            asset class (optional):
                currency (default)
        asset = List[str]
            comma delimited list of assets to get info on (optional)
                default = all for given asset class)
    """

    info: typing.Optional[Literal["info"]]
    aclass: typing.Optional[Literal["currency"]]
    asset: typing.Optional[typing.List[ASSET]]


# ------------------------------
# Response Model
# ------------------------------


def _generate_model(keys: typing.List[str]) -> typing.Type[pydantic.BaseModel]:
    """dynamically create the model. Returns a new pydantic model class
    
    Args:
    ----
        key: List[str]
            List of asset names that map to their info

    """


    class _Asset(pydantic.BaseModel):

        altname: str
        aclass: str
        decimals: int
        display_decimals: int

    # we do not know the keys in advance, only the type of their value
    kwargs = {
        **{k: (_Asset, ...) for k in keys},
        "__base__": pydantic.BaseModel
    }

    model = pydantic.create_model(
        '_AssetsResp',
        **kwargs    #type: ignore
    )

    return model


class AssetsResp:
    """Response Model for endpoint https://api.kraken.com/0/public/Assets

    Model Fields:
    -------
        `asset_name` : dict
            Array of asset name and corresponding info
                altname = alternate name
                aclass = asset class
                decimals = scaling decimal places for record keeping
                display_decimals = scaling decimal places for output display
    """

    def __call__(self, **kwargs):
        model = _generate_model(list(kwargs.keys()))
        print("\nFields", model.__fields__, "\n")
        return model(**kwargs)
