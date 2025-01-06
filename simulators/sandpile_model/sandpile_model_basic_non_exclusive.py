import numpy as np
from enums.placement_type import PlacementType
from enums.stress_introduction_type import StressIntroductionType

class SandpileModel:

    def __init__(self, number_agents=30, grid_size=(20,20), placement_type=PlacementType.RANDOM, stress_threshold=4, 
                 stress_introduction_type=None, num_stress_introduction=None, probability_stress_introduction=None,
                 leaving_threshold=None):
        self.number_agents = number_agents
        self.grid_size = grid_size
        self.placement_type = placement_type
        self.stress_threshold = stress_threshold
        self.stress_introduction_type = stress_introduction_type
        self.num_stress_introduction = num_stress_introduction
        self.probability_stress_introduction = probability_stress_introduction
        self.leaving_threshold = leaving_threshold

        if num_stress_introduction and probability_stress_introduction:
            raise Exception("Cannot impose the number of agents to add stress to and the probability of adding stress at the same time. Please supply only one of these values.")

    def determine_adjacency(self):
        """
        Creates a dictionary of the neighbouring cells of every cell in the cell grid.

        Returns:
            A dictionary with an entry for every cell with an array of the indices of its neighbours as its value.
        """
        adjacent_cells = {}
        for cell_idx in range(self.grid_size[0] * self.grid_size[1]):
            neighbours = [cell_idx] # always check the particle's own cell
            # top if not in top row
            if cell_idx % self.grid_size[1] != 0:
                neighbours.append(cell_idx-1)
                # corner up left
                if cell_idx >= self.grid_size[1]:
                    neighbours.append(cell_idx - self.grid_size[1] -1)
                # corner up right
                if cell_idx < ((self.grid_size[0]*self.grid_size[1]) - self.grid_size[1]):
                    neighbours.append(cell_idx + self.grid_size[1] - 1) 
            # bottom if not in bottom row
            if cell_idx % self.grid_size[1] != (self.grid_size[1]-1):
                neighbours.append(cell_idx+1)
                # corner bottom left
                if cell_idx >= self.grid_size[1]:
                    neighbours.append(cell_idx - self.grid_size[1] + 1)
                # corner bottom right
                if cell_idx < ((self.grid_size[0]*self.grid_size[1]) - self.grid_size[1]):
                    neighbours.append(cell_idx + self.grid_size[1] + 1)
            # left if not in leftmost row
            if cell_idx >= self.grid_size[1]:
                neighbours.append(cell_idx-self.grid_size[1])
            # right if not in rightmost row
            if cell_idx < ((self.grid_size[0]*self.grid_size[1]) - self.grid_size[1]):
                neighbours.append(cell_idx+self.grid_size[1])   
            adjacent_cells[cell_idx] = neighbours    
        self.adjacent_cells = adjacent_cells

    def is_cell_on_border(self, cell_idx):
        is_left = cell_idx < self.grid_size[0]
        is_right = cell_idx > (self.grid_size[0] * (self.grid_size[1]-1))
        is_top = cell_idx % self.grid_size[0] == 0
        is_bottom = cell_idx % self.grid_size[0] == (self.grid_size[1]-1)
        return is_left or is_right or is_top or is_bottom

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

    def compute_stress_levels_from_neighbours(self):
        stress_levels = np.zeros(self.number_agents)
        for i in range(self.number_agents):
            if self.placements[i] < 0:
                continue
            else:
                neighbouring_cells = self.adjacent_cells[self.placements[i]]
                stress_levels[i] = np.sum([len(self.grid[neighbour_cell]) for neighbour_cell in neighbouring_cells])
        return stress_levels
    
    def check_stress_levels(self, stress_levels):
        passed_threshold = stress_levels > self.stress_threshold
        indices = np.nonzero(passed_threshold)[0]
        if len(indices) > 0:
            for i in indices:
                current_cell = self.placements[i]

                if self.placements[i] < 0:
                    continue # if the agent has already left, we don't care anymore

                if self.leaving_threshold and stress_levels[i] > self.leaving_threshold and self.is_cell_on_border(current_cell):
                    self.placements[i] = -current_cell
                else:
                    neighbour_density = {neighbour_cell: len(self.grid[neighbour_cell]) for neighbour_cell in self.adjacent_cells[current_cell]}
                    new_cell = min(neighbour_density, key=neighbour_density.get)
                    self.grid[new_cell].append(i)
                    self.placements[i] = new_cell

                self.grid[current_cell].remove(i)

    def introduce_stress(self, stress_levels_intrinsic):
        if self.num_stress_introduction:
            selected_agents = np.random.choice(self.number_agents, self.num_stress_introduction)
        elif self.probability_stress_introduction:
            rands = np.random.random(self.number_agents)
            selected_agents = np.nonzero(rands <= self.probability_stress_introduction)
        match self.stress_introduction_type:
            case StressIntroductionType.INT_POSITIVE_ONLY:
                stress_levels_intrinsic[selected_agents] += 1
            case StressIntroductionType.INT_POS_NEG:
                rands = np.random.choice([-1, 1], len(selected_agents))
                stress_levels_intrinsic[selected_agents] += rands
            case StressIntroductionType.FLOAT_POSITIVE_ONLY:
                rands = np.random.random(len(selected_agents))
                stress_levels_intrinsic[selected_agents] += rands
            case StressIntroductionType.FLOAT_POS_NEG:
                rands = np.random.random(len(selected_agents))
                rand_pos_neg = np.random.random(len(selected_agents))
                for i in range(len(selected_agents)):
                    if rand_pos_neg[i] < 0.5:
                        rands[i] *= -1
                stress_levels_intrinsic[selected_agents] += rands
        return stress_levels_intrinsic
    
    def get_stress_density_matrix(self):
        stress_mat = np.zeros((self.grid_size[0], self.grid_size[1]))
        for cell in self.grid.keys():
            x = cell % self.grid_size[0]
            y = int((cell-x) / self.grid_size[0])
            stress_mat[x][y] = len(self.grid[cell])
        return stress_mat


    def simulate(self, tmax=1000, dt=1):
        self.initialise_grid()

        placement_history = np.zeros((tmax,self.number_agents))
        stress_density_history = np.zeros((tmax, self.grid_size[0], self.grid_size[1]))
        stress_level_history = np.zeros((tmax, self.number_agents))

        stress_levels_intrinsic = np.zeros(self.number_agents)
        stress_levels_neighbours = self.compute_stress_levels_from_neighbours()
        stress_levels = stress_levels_neighbours + stress_levels_intrinsic

        placement_history[0,:] = np.array(list(self.placements.values()))
        stress_density_history[0,:,:] = self.get_stress_density_matrix()
        stress_level_history[0,:] = stress_levels

        for t in range(1, tmax):
            self.t = t

            stress_levels_intrinsic = self.introduce_stress(stress_levels_intrinsic=stress_levels_intrinsic)
            
            stress_levels_neighbours = self.compute_stress_levels_from_neighbours()
            stress_levels = stress_levels_neighbours + stress_levels_intrinsic

            self.check_stress_levels(stress_levels)

            placement_history[t,:] = np.array(list(self.placements.values()))
            stress_density_history[t,:,:] = self.get_stress_density_matrix()
            stress_level_history[t,:] = stress_levels

        return (dt*np.arange(tmax), placement_history, stress_density_history, stress_level_history)
        


