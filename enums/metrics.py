from enum import Enum

"""
Indicates which particles should be coloured during the experiment to facilitate better understanding in the video rendering.
"""
class Metrics(str, Enum):
    LONGEST_SURVIVAL = "LS",
    NUMBER_OF_SURVIVORS_AT_FINAL_TIMESTEP = "NSFT"