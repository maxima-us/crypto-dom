import re
import typing
from decimal import Decimal

from typing_extensions import Literal

from crypto_dom.definitions import Nstr, TIMESTAMP_S



#------------------------------------------------------------
# Pairs
#------------------------------------------------------------

try:
    from ._definitions_assetpairs import PAIR
    PAIR = PAIR
except ImportError:
    PAIR = str


PAIR_FIAT = Literal[
    "USD",
    "EUR",
    "GBP",
    "JPY",
    "CHF",
    "CAD"
]


#------------------------------------------------------------
# Assets
#------------------------------------------------------------


try: 
    from ._definitions_assets import ASSET
except ImportError:
    ASSET = str


ASSETCLASS = Literal["currency"]    #TODO verify this


#------------------------------------------------------------
# TImeframes
#------------------------------------------------------------


TIMEFRAME = Literal[1, 5, 15, 30, 60, 240, 1440, 10080, 21600]


#------------------------------------------------------------
# Flags
#------------------------------------------------------------


class FLAGS(Nstr):
    regex = re.compile(r'((viqc|fcib|fciq|nompp|post)+?)(?:,|$)')
    strict = True


#------------------------------------------------------------
# Orders
#------------------------------------------------------------


ORDERTYPE = Literal["market", "limit", "stop-loss", "take-profit", "stop-loss-limit", "take-profit-limit", "settle-position", "stop market"]

ORDERSIDE = Literal["buy", "sell"]

ORDERSTATUS = Literal["pending", "open", "closed", "canceled", "expired"]


#------------------------------------------------------------
# IDs
#------------------------------------------------------------


class KrakenID(Nstr):
    regex = re.compile(r'^[A-Z0-9]{6}-[A-Z0-9]{5}-[A-Z0-9]{6}$')
    strict = True


class TRADEID(KrakenID): pass

class ORDERID(KrakenID): pass

class LEDGERID(KrakenID): pass


#------------------------------------------------------------
# Margin
#------------------------------------------------------------


LEVERAGE = Literal[0,1,2,3,4,5]


#------------------------------------------------------------
# Endpoint specific
#------------------------------------------------------------
   
   
# Entries(<time>, <open>, <high>, <low>, <close>, <vwap>, <volume>, <count>)
CANDLE = typing.Tuple[Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, Decimal, int]

# tuple of price, volume, time
BID = typing.Tuple[Decimal, Decimal, TIMESTAMP_S]
ASK = typing.Tuple[Decimal, Decimal, TIMESTAMP_S]

ASKS = typing.Tuple[ASK, ...]
BIDS = typing.Tuple[BID, ...]

# array of array entries(<time>, <bid>, <ask>)
SPREAD = typing.Tuple[TIMESTAMP_S, Decimal, Decimal]
