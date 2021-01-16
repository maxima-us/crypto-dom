import re

from typing_extensions import Literal

from crypto_dom.definitions import Nstr

#------------------------------------------------------------
# Pairs
#------------------------------------------------------------

try:
    from ._definitions_assetpairs import PAIR
    PAIR = PAIR
except ImportError:
    PAIR = str


#------------------------------------------------------------
# Assets
#------------------------------------------------------------


try: 
    from ._definitions_assets import ASSET
except ImportError:
    ASSET = str


#------------------------------------------------------------
# TImeframes
#------------------------------------------------------------


TIMEFRAME = Literal[1, 5, 15, 30, 60, 240, 1440, 10080, 21600]


#------------------------------------------------------------
# Flags
#------------------------------------------------------------


FLAGS = Literal["viqc", "fcib", "fciq", "nompp"]


#------------------------------------------------------------
# Orders
#------------------------------------------------------------


ORDERTYPE = Literal["market", "limit", "stop-loss", "take-profit", "stop-loss-limit", "take-profit-limit", "settle-position", "stop market"]

ORDERSIDE = Literal["buy", "sell"]

ORDERSTATUS = Literal["pending", "open", "closed", "canceled", "expired"]


#------------------------------------------------------------
# IDs
#------------------------------------------------------------

class TRADEID(Nstr):
    regex = re.compile(r'^[A-Z0-9]{6}-[A-Z0-9]{5}-[A-Z0-9]{6}$')
    strict = True


class ORDERID(Nstr):
    regex = re.compile(r'^[A-Z0-9]{6}-[A-Z0-9]{5}-[A-Z0-9]{6}$')
    strict = True


