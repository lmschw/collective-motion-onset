from enum import Enum

"""
Indicates which particles should be coloured during the experiment to facilitate better understanding in the video rendering.
"""
class PlacementTypePrey(str, Enum):
    EQUIDISTANT = "EQ",
    RANDOM = "R"

class PlacementTypePredator(str, Enum):
    BORDER = "B",
    CENTER = "C",
    RANDOM = "R"