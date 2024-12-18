from enum import Enum

"""
Indicates which particles should be coloured during the experiment to facilitate better understanding in the video rendering.
"""
class StressIntroductionType(str, Enum):
    INT_POSITIVE_ONLY = "INTP",
    INT_POS_NEG = "INTPN",
    FLOAT_POSITIVE_ONLY = "FLP",
    FLOAT_POS_NEG = "FLPN"