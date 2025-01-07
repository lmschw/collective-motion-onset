from enum import Enum

"""
Indicates which particles should be coloured during the experiment to facilitate better understanding in the video rendering.
"""
class AgentType(Enum):
    PREDATOR = "H", "r"
    PREY = "P", "b"

    def __init__(self, label, colour):
        self.label = label
        self.colour = colour