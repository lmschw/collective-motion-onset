from enum import Enum

"""
Indicates which particles should be coloured during the experiment to facilitate better understanding in the video rendering.
"""
class PredatorBehaviour(str, Enum):
    NEAREST_PREY = "NP"