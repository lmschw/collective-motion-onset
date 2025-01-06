import numpy as np

from enums.placement_type import PlacementType
from enums.cell_visibility import CellVisibility

import services.service_grid as sgrid

class SandpileModel:

    def __init__(self, number_agents, grid_size, model, placement_type, cell_visibility):
        self.number_agents = number_agents
        self.grid_size = grid_size
        self.model = model
        self.placement_type = placement_type
        self.cell_visibility = cell_visibility


    def determine_adjacency(self):
        """
        Creates a dictionary of the neighbouring cells of every cell in the cell grid.

        Returns:
            A dictionary with an entry for every cell with an array of the indices of its neighbours as its value.
        """
        adjacent_cells = {}
        for cell_idx in range(self.grid_size[0] * self.grid_size[1]):
            match self.cell_visibility:
                case CellVisibility.CROSS_ONE:
                    top, right, bottom, left = sgrid.get_adjacent_cross_cells_distance_one(cell_idx=cell_idx, grid_size=self.grid_size)
                    adjacent_cells[cell_idx] = [top, right, bottom, left]
                case CellVisibility.SQUARE_EIGHT:
                    adjacent_cells[cell_idx] = sgrid.get_adjacent_square_cells_eight(cell_idx=cell_idx, grid_size=self.grid_size)
        self.adjacent_cells = adjacent_cells

    def get_adjacent_values(self, cell_idx):
        pass

    def initialise_grid(self):
        grid = {i: [] for i in range(self.grid_size[0] * self.grid_size[1])}
        placements = {}
        match self.placement_type:
            case PlacementType.EQUIDISTANT:
                pass
            case PlacementType.RANDOM:
                rand_x = np.random.randint(0, self.grid_size[0], self.number_agents)
                rand_y = np.random.randint(0, self.grid_size[1], self.number_agents)
                for i in range(self.number_agents):
                    cell = rand_y[i] * self.grid_size[0] + rand_x[i]
                    grid[cell].append(i)
                    placements[i] = cell
        self.grid = grid
        self.placements = placements
        self.determine_adjacency()



    def get_neighbourhood(self):
        neighbours = np.zeros((self.number_agents, self.cell_visibility.number_cells))
        for i in range(self.number_agents):
            neighbours[i] = self.get_adjacent_values(self.placements[i])
                    

    def make_moves(self):
        pass

    def simulate(self, tmax=1000, dt=1):
        pass

