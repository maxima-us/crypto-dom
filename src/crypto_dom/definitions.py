import pydantic


#------------------------------------------------------------
# Base Types
#------------------------------------------------------------


class NFloat(pydantic.ConstrainedInt):

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
# Count
#------------------------------------------------------------


class COUNT(NInt):
    ge=0
    strict=False


#------------------------------------------------------------
# Timestamps
#------------------------------------------------------------


class Gt0Float(NFloat):
    ge=0.0
    strict=False


TIMESTAMP_S = Gt0Float
TIMESTAMP_MS = Gt0Float
TIMESTAMP_NS = Gt0Float