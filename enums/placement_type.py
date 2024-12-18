from enum import Enum

"""
Indicates which particles should be coloured during the experiment to facilitate better understanding in the video rendering.
"""
class PlacementType(str, Enum):
    EQUIDISTANT = "EQ",
    RANDOM = "R"