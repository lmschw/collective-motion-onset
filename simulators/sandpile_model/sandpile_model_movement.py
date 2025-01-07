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
    
    def get_agent_by_id(self, id):
        agent = None
        for a in self.agents:
            if a.id == id:
                agent = a
                break
        return agent
    
    def remove_prey_by_id(self, agent_id, cell_idx):
        # note: will not do anything if the agent is not in that cell
        candidates = self.grid[cell_idx]["prey"]
        updated = []
        for cand in candidates:
            if cand.id != agent_id:
                updated.append(cand)
        self.grid[cell_idx]["prey"] = updated
        
    def eliminate_prey(self, cell_idx):
        preys = self.grid[cell_idx]["prey"]
        if len(preys) == 0:
            raise Exception("Tried to eliminate a prey but no prey is present")
        victim = np.random.randint(0, len(preys))
        self.remove_prey_by_id(agent_id=victim, cell_idx=cell_idx)
        
    def is_placement_in_cell_allowed(self, cell_idx, agent):
        if agent.agent_type == AgentType.PREDATOR:
            # there cannot be more than the limit of allowed predators
            if len(self.grid[cell_idx]["pred"]) >= self.agents_per_cell_limit:
                return False
            # if there is prey, then the predator can move there and will kill a prey agent
            if len(self.grid[cell_idx]["prey"]) > 0:
                self.eliminate_prey(cell_idx=cell_idx)
                return True
        else:
            # there cannot be more than the limit of allowed prey
            if len(self.grid[cell_idx]["pred"]) + len(self.grid[cell_idx]["prey"]) >= self.agents_per_cell_limit:
                return False
            # if there is a predator, a prey cannot be placed
            if len(self.grid[cell_idx]["pred"]) > 0:
                return False
        return True
    
    def place_predator(self, predator):
        pass

    def place_prey(self, prey):
        pass
    
    def place_agent(self, agent):
        if agent.agent_type == AgentType.PREDATOR:
            self.place_predator(agent)
        else:
            self.place_prey(agent)

    def initialise_agents(self):
        self.agents = []
        max_id = 0
        while max_id <= (self.num_agents + self.num_predators):
            if max_id <= self.num_predators:
                agent = Agent(id=max_id, agent_type=AgentType.PREDATOR)
            else:
                agent = Agent(id=max_id, agent_type=AgentType.PREY)
            self.agents.append(agent)
            max += 1

    def initialise_grid(self):
        grid = {i: {'pred': [], 'prey': []} for i in range(self.grid_size[0] * self.grid_size[1])}
        self.initialise_agents()
        for agent in self.agents:
            self.place_agent(agent=agent)

        placements_predators = {}
        for predator in range(self.num_predators):
            match self.placement_type_predator:
                case PlacementTypePredator.BORDER:
                    rand = np.random.randint(0,4)
                    match rand:
                        case 0: # first column
                            rand_x = 0
                            rand_y = np.random.randint(0, self.grid_size[1])
                        case 1: # bottom
                            rand_x = np.random.randint(0, self.grid_size[0])
                            rand_y = self.grid_size[0]
                        case 2: # last column
                            rand_x = self.grid_size[0]
                            rand_y = np.random.randint(0, self.grid_size[1])
                        case 3: # top
                            rand_x = np.random.randint(0, self.grid_size[0])
                            rand_y = 0
                    cell = rand_y[i] * self.grid_size[0] + rand_x[i]
                    grid[cell]['pred'].append(i)
                    placements_predators[i] = cell

        placements_prey = {}
        match self.placement_type_prey:
            case PlacementTypePrey.EQUIDISTANT:
                pass
            case PlacementTypePrey.RANDOM:
                rand_x = np.random.randint(0, self.grid_size[0], self.num_agents)
                rand_y = np.random.randint(0, self.grid_size[1], self.num_agents)
                for i in range(self.num_agents):
                    cell = rand_y[i] * self.grid_size[0] + rand_x[i]
                    grid[cell]['prey'].append(i)
                    placements_prey[i] = cell
        self.grid = grid
        self.placements_prey = placements_prey
        self.determine_adjacency()

    def get_neighbourhood(self):
        neighbours = np.zeros((self.num_agents, self.cell_visibility.number_cells))
        for i in range(self.num_agents):
            neighbours[i] = self.get_adjacent_values(self.pl[i])
                    

    def make_moves(self):
        pass

    def simulate(self, tmax=1000, dt=1):
        pass

