import re

import pydantic


#------------------------------------------------------------
# Base Types
#------------------------------------------------------------


class NFloat(pydantic.ConstrainedFloat):

    def __init__(self, _value: float):
        self._value = _value

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self._value}>"


class NInt(pydantic.ConstrainedInt):

    def __init__(self, _value: int):
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
# Counting
#------------------------------------------------------------


class COUNT(NInt):
    ge=0
    strict=False


#------------------------------------------------------------
# Percentages
#------------------------------------------------------------


class PERCENT(NInt):
    ge=0
    le=100
    strict=False


#------------------------------------------------------------
# Timestamps
#------------------------------------------------------------


class Gt0Float(NFloat):
    ge=0.0
    strict=False

class Gt0Int(NInt):
    ge=0
    strict=False

class _IntTimestamp(Gt0Int):
    pass

class _FloatTimestamp(Gt0Float):
    pass

TIMESTAMP_S = _FloatTimestamp 
TIMESTAMP_MS = _IntTimestamp
TIMESTAMP_NS = _IntTimestamp


#------------------------------------------------------------
# Symbols/Pairs and Assets
#------------------------------------------------------------


# pydantic symbol
#   type will only be checked upon validation of a 
#   pydantic model which has a field of the present type
class R_SYMBOL(Nstr):
    regex=re.compile(r'[A-Z0-9]+-[A-Z]+')
    strict=True

# pydantic asset
#   type will only be checked upon validation of a 
#   pydantic model which has a field of the present type
class R_ASSET(Nstr):
    regex=re.compile(r'^[A-Z0-9]{2,10}$')
    strict=True
