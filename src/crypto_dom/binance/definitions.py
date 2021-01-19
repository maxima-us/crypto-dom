import re

from typing_extensions import Literal

from crypto_dom.definitions import Nstr


#------------------------------------------------------------
# Pairs
#------------------------------------------------------------

# try:
#     from ._definitions_assetpairs import PAIR
#     PAIR = PAIR
# except ImportError:
#     PAIR = str


#------------------------------------------------------------
# Assets
#------------------------------------------------------------


# try: 
#     from ._definitions_assets import ASSET
# except ImportError:
#     ASSET = str


#------------------------------------------------------------
# TImeframes
#------------------------------------------------------------


TIMEFRAME = Literal["1m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]


#------------------------------------------------------------
# Symbols
#------------------------------------------------------------


SYMBOL_STATUS = Literal["PRE_TRADING", "TRADING", "POST_TRADING", "END_OF_DAY", "HALT", "AUCTION_MATCH", "BREAK"]

# ? can this also be None ?
SYMBOL_TYPE = Literal["SPOT"] 


#------------------------------------------------------------
# Orders
#------------------------------------------------------------


ORDER_TYPE = Literal["MARKET", "LIMIT", "STOP_LOSS", "TAKE_PROFIT", "STOP_LOSS_LIMIT", "TAKE_PROFIT_LIMIT", "LIMIT_MAKER"]

ORDER_SIDE = Literal["BUY", "SELL"]

ORDER_STATUS = Literal["NEW", "PARTIALLY_FILLED", "FILLED", "CANCELED", "PENDING_CANCEL", "REJECTED", "EXPIRED"]

ORDER_RESP_TYPE = Literal["ACK", "RESULT", "FULL"]

ORDER_TIF = Literal["GTC", "IOC", "FOK"]

OCO_STATUS = Literal["RESPONSE", "EXEC_STARTED", "ALL_DONE"]

OCO_ORDER_STATUS = Literal["EXECUTING", "ALL_DONE", "REJECT"]


#------------------------------------------------------------
# Rate Limiters
#------------------------------------------------------------


RATE_LIMITE_TYPE = Literal["REQUEST_WEIGHT", "ORDERS", "RAW_REQUEST"]

RATE_LIMITE_INTERVAL = Literal["SECOND", "MINUTE", "DAY"]


#------------------------------------------------------------
# IDs
#------------------------------------------------------------


class KrakenID(Nstr):
    regex = re.compile(r'^[A-Z0-9]{6}-[A-Z0-9]{5}-[A-Z0-9]{6}$')
    strict = True


class TRADEID(KrakenID): pass

class ORDERID(KrakenID): pass

class LEDGERID(KrakenID): pass




