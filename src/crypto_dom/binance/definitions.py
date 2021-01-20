import re

from typing_extensions import Literal

from crypto_dom.definitions import NInt, Nstr


#------------------------------------------------------------
# Symbols (Pairs)
#------------------------------------------------------------


try:
    from ._definitions_symbols import SYMBOL
except ImportError:
    SYMBOL = str


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


TIMEFRAME = Literal["1m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]


#------------------------------------------------------------
# Symbols
#------------------------------------------------------------


SYMBOL_STATUS = Literal["PRE_TRADING", "TRADING", "POST_TRADING", "END_OF_DAY", "HALT", "AUCTION_MATCH", "BREAK"]

# ? can this also be None ?
SYMBOL_TYPE = Literal["SPOT"] 

SYMBOL_PERMISSIONS = Literal["SPOT", "MARGIN", "LEVERAGED"]


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


RATE_LIMIT_TYPE = Literal["REQUEST_WEIGHT", "ORDERS", "RAW_REQUEST"]

RATE_LIMIT_INTERVAL = Literal["SECOND", "MINUTE", "DAY"]


#------------------------------------------------------------
# Recv Window
#------------------------------------------------------------


class RECV_WINDOW(NInt):
    ge=0
    le=60000
    strict=False



