import re

from typing_extensions import Literal


TIMEFRAMES = Literal[1, 5, 15, 30, 60, 240, 1440, 10000, 21600]

ORDERTYPE = Literal["market", "limit", "stop-loss", "take-profit", "stop-loss-limit", "take-profit-limit", "settle-position", "stop market"]

ORDERSIDE = Literal["buy", "sell"]

ORDERSTATUS = Literal["pending", "open", "closed", "canceled", "expired"]

FLAGS = Literal["viqc", "fcib", "fciq", "nompp"]


#! MOVE BELOW BACK TO BASE/DEFINITIONS WHEN DONE WITH KRAKEN AND WHEN WE HAVE A SETUP.PY
import pydantic



#------------------------------------------------------------
# Base Types
#------------------------------------------------------------

class NInt(pydantic.ConstrainedInt):

    def __init__(self, _value: int):
        self._value = _value

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self._value}>"

class NFloat(pydantic.ConstrainedFloat):

    def __init__(self, _value: float):
        self._value = _value

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self._value}>"

class Nstr(pydantic.ConstrainedStr):


    def __init__(self, _value: str):
        self._value = _value

    def __str__(self):
        # we want to be able to concat strings
        return self._value

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self._value}>"


#------------------------------------------------------------
# Timestamps
#------------------------------------------------------------

class Gt0Float(NFloat):
    ge=0.0
    strict=False


TIMESTAMP_S = Gt0Float
TIMESTAMP_MS = Gt0Float
TIMESTAMP_NS = Gt0Float


#------------------------------------------------------------
# Count
#------------------------------------------------------------

class COUNT(NInt):
    ge=0
    strict=False


#------------------------------------------------------------
# IDs
#------------------------------------------------------------

class TRADEID(Nstr):
    regex = re.compile(r'^[A-Z0-9]{6}-[A-Z0-9]{5}-[A-Z0-9]{6}$')
    strict = True


class ORDERID(Nstr):
    regex = re.compile(r'^[A-Z0-9]{6}-[A-Z0-9]{5}-[A-Z0-9]{6}$')
    strict = True


