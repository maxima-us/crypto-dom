import re

from typing_extensions import Literal

from crypto_dom.definitions import Nstr


TIMEFRAMES = Literal[1, 5, 15, 30, 60, 240, 1440, 10000, 21600]

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


