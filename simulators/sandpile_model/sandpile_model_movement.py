import numpy as np

from enums.agent_type import AgentType
from enums.cell_visibility import CellVisibility
from enums.placement_type import PlacementTypePrey, PlacementTypePredator
from enums.predator_behaviour import PredatorBehaviour
from models.agents import Agent
import services.service_grid as sgrid

class SandpileModel:

    def __init__(self, num_agents, grid_size, model, placement_type_prey, cell_visibility, num_directions=4, allow_stay=True,
                 agents_per_cell_limit=2, num_predators=1, predator_behaviour=PredatorBehaviour.NEAREST_PREY, 
                 placement_type_predator=PlacementTypePredator.RANDOM):
        self.num_agents = num_agents
        self.grid_size = grid_size
        self.model = model
        self.placement_type_prey = placement_type_prey
        self.cell_visibility = cell_visibility
        self.num_directions = num_directions
        self.allow_stay = allow_stay
        self.agents_per_cell_limit = agents_per_cell_limit
        self.num_predators = num_predators
        self.predator_behaviour = predator_behaviour
        self.placement_type_predator = placement_type_predator

        self.agents = [i for i in range(self.num_agents + self.num_predators)]

        self.initialise_grid()

    def print_grid(self):
        line = "".join([f"\t{i}" for i in range(self.grid_size[1])])
        print(line)
        for x in range(self.grid_size[0]):
            line = f"{x}"
            for y in range(self.grid_size[1]):
                cell_idx = sgrid.get_grid_cell_idx(x=x, y=y, grid_size=self.grid_size)
                preys = self.get_prey_ids(cell_idx=cell_idx)
                predators = self.get_predator_ids(cell_idx=cell_idx)
                prey_string = "".join([f"P{i}" for i in preys])
                predator_string = "".join([f"H{i}" for i in predators])
                line += f"\t{predator_string}{prey_string}"
            print(line)

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
        return [self.grid[cell] for cell in self.adjacent_cells[cell_idx]]
    
    def is_predator(self, agent_id):
        return agent_id < self.num_predators
    
    def is_prey(self, agent_id):
        return not self.is_predator(agent_id=agent_id)
    
    def get_predator_ids(self, cell_idx):
        cell = np.array(self.grid[cell_idx])
        return cell[cell < self.num_predators]
    
    def get_prey_ids(self, cell_idx):
        cell = np.array(self.grid[cell_idx])
        return cell[cell >= self.num_predators]
    
    def remove_prey_from_cell_by_id(self, agent_id, cell_idx):
        # note: will not do anything if the agent is a predator
        if agent_id < self.num_predators: # i.e. it is a prey
            self.grid[cell_idx].remove(agent_id)
            self.placements.pop(agent_id)
            self.agents.remove(agent_id)
        
    def eliminate_prey(self, cell_idx):
        preys = self.get_prey_ids(cell_idx=cell_idx)
        if len(preys) == 0:
            raise Exception("Tried to eliminate a prey but no prey is present")
        victim = np.random.randint(0, len(preys))
        self.remove_prey_from_cell_by_id(agent_id=victim, cell_idx=cell_idx)
        
    def is_placement_in_cell_allowed(self, cell_idx, agent_id, is_check_only=False):
        preys = self.get_prey_ids(cell_idx=cell_idx)
        predators = self.get_predator_ids(cell_idx=cell_idx)
        # if it is a predator
        if self.is_predator(agent_id=agent_id):
            # there cannot be more than the limit of allowed predators
            if len(predators) >= self.agents_per_cell_limit:
                return False
            # if there is prey, then the predator can move there and will kill a prey agent
            if len(preys) > 0:
                if not is_check_only:
                    self.eliminate_prey(cell_idx=cell_idx)
                return True
        else: # if it is a prey
            # there cannot be more than the limit of allowed prey
            if len(preys) >= self.agents_per_cell_limit:
                return False
            # if there is a predator, a prey cannot be placed
            if len(predators) > 0:
                return False
        return True
    
    def __choose_x_y_on_border(self):
        rand = np.random.randint(0,4)
        match rand:
            case 0: # first column
                x = 0
                y = np.random.randint(0, self.grid_size[1])
            case 1: # bottom
                x = np.random.randint(0, self.grid_size[0])
                y = self.grid_size[0]-1
            case 2: # last column
                x = self.grid_size[0]-1
                y = np.random.randint(0, self.grid_size[1])
            case 3: # top
                x = np.random.randint(0, self.grid_size[0])
                y = 0
        return x, y
    
    def place_predator(self, agent_id):
        match self.placement_type_predator:
            case PlacementTypePredator.BORDER:
                x, y = self.__choose_x_y_on_border()
                while not self.is_placement_in_cell_allowed(cell_idx=sgrid.get_grid_cell_idx(x=x, y=y, grid_size=self.grid_size), agent_id=agent_id):
                    x, y = self.__choose_x_y_on_border()
            case PlacementTypePredator.CENTER:
                x = np.floor(self.grid_size[0]/2)
                y = np.floor(self.grid_size[1]/2)
                round = 0
                combination_counter = 0
                increasing = True
                using_x = True
                while not self.is_placement_in_cell_allowed(cell_idx=sgrid.get_grid_cell_idx(x=x, y=y, grid_size=self.grid_size), agent_id=agent_id):
                    if increasing and using_x:
                        x += 1
                        if combination_counter >= round:
                            using_x = False
                            combination_counter = 0
                        else:
                            combination_counter += 1
                    elif increasing and not using_x:
                        y += 1
                        if combination_counter >= round:
                            using_x = True
                            combination_counter = 0
                            increasing = False
                        else:
                            combination_counter += 1
                    elif using_x:
                        x -= 1
                        if combination_counter > round:
                            using_x = False
                            combination_counter = 0
                        else:
                            combination_counter += 1
                    else:
                        y -= 1
                        if combination_counter > round:
                            using_x = True
                            combination_counter = 0
                            increasing = True
                            round += 2
                        else:
                            combination_counter += 1
            case PlacementTypePredator.RANDOM:
                x = np.random.randint(0, self.grid_size[0])
                y = np.random.randint(0, self.grid_size[1])
                while not self.is_placement_in_cell_allowed(cell_idx=sgrid.get_grid_cell_idx(x=x, y=y, grid_size=self.grid_size), agent_id=agent_id):
                    x = np.random.randint(0, self.grid_size[0])
                    y = np.random.randint(0, self.grid_size[1])

        cell = sgrid.get_grid_cell_idx(x=x, y=y, grid_size=self.grid_size)
        self.grid[cell].append(agent_id)
        self.placements[agent_id] = cell

    def place_prey(self, agent_id):
        match self.placement_type_prey:
            case PlacementTypePrey.EQUIDISTANT:
                # TODO: implement equidistant placement of pry
                raise Exception("EQUIDISTANT has not been implemented yet")
            case PlacementTypePrey.RANDOM:
                x = np.random.randint(0, self.grid_size[0])
                y = np.random.randint(0, self.grid_size[1])
                while not self.is_placement_in_cell_allowed(cell_idx=sgrid.get_grid_cell_idx(x=x, y=y, grid_size=self.grid_size), agent_id=agent_id):
                    x = np.random.randint(0, self.grid_size[0])
                    y = np.random.randint(0, self.grid_size[1])

        cell = sgrid.get_grid_cell_idx(x=x, y=y, grid_size=self.grid_size)
        self.grid[cell].append(agent_id)
        self.placements[agent_id] = cell
    
    def place_agent(self, agent_id):
        if self.is_predator(agent_id=agent_id):
            self.place_predator(agent_id=agent_id)
        else:
            self.place_prey(agent_id=agent_id)

    def initialise_grid(self):
        self.grid = {i: [] for i in range(self.grid_size[0] * self.grid_size[1])}
        self.determine_adjacency()
        self.placements = {i: -1 for i in range(len(self.agents))}
        for agent in self.agents:
            self.place_agent(agent_id=agent)            

    def get_neighbourhood(self):
        neighbours = np.zeros((self.num_agents, self.cell_visibility.number_cells))
        for i in range(self.num_agents):
            neighbours[i] = self.get_adjacent_values(self.pl[i])
                    

    def make_moves(self):
        pass

    def simulate(self, tmax=1000, dt=1):
        pass

