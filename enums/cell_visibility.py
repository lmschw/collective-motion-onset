from enum import Enum

"""
Indicates which particles should be coloured during the experiment to facilitate better understanding in the video rendering.
"""
class CellVisibility(Enum):
    CROSS_ONE = "C1", 4,
    SQUARE_EIGHT = "S8", 8

    def __init__(self, label, number_cells):
        self.label = label
        self.number_cells = number_cells
