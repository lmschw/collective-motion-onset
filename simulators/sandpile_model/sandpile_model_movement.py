import numpy as np
import copy

from enums.agent_type import AgentType
from enums.cell_visibility import CellVisibility
from enums.placement_type import PlacementTypePrey, PlacementTypePredator
from enums.predator_behaviour import PredatorBehaviour
from models.agents import Agent
import services.service_grid as sgrid
import services.service_helper as shelp

class SandpileModel:

    def __init__(self, num_agents, grid_size, model, placement_type_prey, cell_visibility, allow_stay=True,
                 agents_per_cell_limit=2, num_predators=1, predator_behaviour=PredatorBehaviour.NEAREST_PREY, 
                 placement_type_predator=PlacementTypePredator.RANDOM, predator_random_movement_after=50):
        self.num_agents = num_agents
        self.grid_size = grid_size
        self.model = model
        self.placement_type_prey = placement_type_prey
        self.cell_visibility = cell_visibility
        self.allow_stay = allow_stay
        self.agents_per_cell_limit = agents_per_cell_limit
        self.num_predators = num_predators
        self.predator_behaviour = predator_behaviour
        self.placement_type_predator = placement_type_predator
        self.predator_random_movement_after = predator_random_movement_after

        self.agents = [i for i in range(self.num_agents + self.num_predators)]
        self.last_predator_movements = np.zeros(self.num_predators)

        # TODO: replace with an enum to allow movement other than cross
        self.num_directions = 4
        self.directions = [i for i in range(self.num_directions)]
        if self.allow_stay:
            self.directions.append(self.num_directions + 1)

    def get_model_params(self):
        return {
            "n": self.num_agents,
            "grid_size": self.grid_size,
            "placement_type_prey": self.placement_type_prey.name,
            "cell_visibility": self.cell_visibility.name,
            "allow_stay": self.allow_stay,
            "agents_per_cell_limit": self.agents_per_cell_limit,
            "num_predators": self.num_predators,
            "predator_behaviour": self.predator_behaviour.name,
            "placement_type_predator": self.placement_type_predator.name,
            "predator_random_movement_after": self.predator_random_movement_after,
            "model_summary": self.model.get_model_summary()
        }

    def print_grid(self):
        line = "".join([f"\t{i}" for i in range(self.grid_size[1])])
        print(line)
        for x in range(self.grid_size[0]):
            line = f"{x}"
            for y in range(self.grid_size[1]):
                cell_idx = sgrid.get_grid_cell_idx(x=x, y=y, grid_size=self.grid_size)
                preys = self.get_prey_ids_from_cell(cell_idx=cell_idx)
                predators = self.get_predator_ids_from_cell(cell_idx=cell_idx)
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
    
    def get_predators_ids_from_list(self, list):
        arr = np.array(list)
        return arr[arr < self.num_predators]
    
    def get_predator_ids_from_cell(self, cell_idx):
        cell = np.array(self.grid[cell_idx])
        return cell[cell < self.num_predators]
    
    def get_prey_ids_from_list(self, list):
        arr = np.array(list)
        return arr[arr >= self.num_predators]
    
    def get_prey_ids_from_cell(self, cell_idx, grid=None):
        cell = np.array(self.grid[cell_idx])
        return cell[cell >= self.num_predators]
    
    def remove_prey_from_cell_by_id(self, agent_id, cell_idx):
        # note: will not do anything if the agent is a predator
        if self.is_prey(agent_id=agent_id): # i.e. it is a prey
            self.grid[cell_idx].remove(agent_id)
            self.placements.pop(agent_id)
            self.agents.remove(agent_id)
        
    def eliminate_prey_from_cell(self, cell_idx):
        preys = self.get_prey_ids_from_cell(cell_idx=cell_idx)
        if len(preys) == 0:
            raise Exception("Tried to eliminate a prey but no prey is present")
        victim = np.random.choice(preys, 1)[0]
        self.remove_prey_from_cell_by_id(agent_id=victim, cell_idx=cell_idx)

    def eliminate_prey(self):
        for cell_idx in self.grid:
            if len(self.get_predator_ids_from_cell(cell_idx=cell_idx)) > 0 and len(self.get_prey_ids_from_cell(cell_idx=cell_idx)) > 0:
                self.eliminate_prey_from_cell(cell_idx=cell_idx)
        
    def is_placement_in_cell_allowed(self, cell_idx, agent_id):
        preys = self.get_prey_ids_from_cell(cell_idx=cell_idx)
        predators = self.get_predator_ids_from_cell(cell_idx=cell_idx)
        # if it is a predator
        if self.is_predator(agent_id=agent_id):
            # there cannot be more than the limit of allowed predators
            if len(predators) >= self.agents_per_cell_limit:
                return False
            # if there is prey, then the predator can move there and will kill a prey agent
            if len(preys) > 0:
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
    
    def place_predator(self, agent_id, grid, placements):
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
        grid[cell].append(agent_id)
        placements[agent_id] = cell
        return grid, placements

    def place_prey(self, agent_id, grid, placements):
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
        grid[cell].append(agent_id)
        placements[agent_id] = cell
        return grid, placements
    
    def place_agent(self, agent_id, grid, placements):
        if self.is_predator(agent_id=agent_id):
            return self.place_predator(agent_id=agent_id, grid=grid, placements=placements)
        else:
            return self.place_prey(agent_id=agent_id, grid=grid, placements=placements)

    def initialise_grid(self):
        grid = {i: [] for i in range(self.grid_size[0] * self.grid_size[1])}
        self.determine_adjacency()
        placements = {i: -1 for i in range(len(self.agents))}
        for agent in self.agents:
            self.grid = grid
            grid, placements = self.place_agent(agent_id=agent, grid=grid, placements=placements) 
        return grid, placements          

    def get_neighbourhood(self, agent_id):
        neighbourhood = np.zeros(self.cell_visibility.number_cells)
        neighbours = self.get_adjacent_values(self.placements[agent_id])
        for neighbour_idx in range(self.cell_visibility.number_cells):
            preys = self.get_prey_ids_from_list(neighbours[neighbour_idx])
            predators = self.get_predators_ids_from_list(neighbours[neighbour_idx])
            neighbourhood[neighbour_idx] = len(preys) + 3 * len(predators)
        return neighbourhood
    
    def pick_predator_direction(self, agent_id):
        match self.predator_behaviour:
            case PredatorBehaviour.NEAREST_PREY:
                adjacent_cells = self.get_adjacent_values(cell_idx=self.placements[agent_id])
                if self.cell_visibility == CellVisibility.CROSS_ONE:
                    for cell in range(len(adjacent_cells)):
                        preys = self.get_prey_ids_from_list(adjacent_cells[cell])
                        if len(preys) > 0 and self.is_placement_in_cell_allowed(cell_idx=self.adjacent_cells[self.placements[agent_id]][cell], agent_id=agent_id):
                            return cell
                if self.cell_visibility == CellVisibility.SQUARE_EIGHT:
                    for cell in range(0, len(adjacent_cells), 2):
                        preys = self.get_prey_ids_from_list(adjacent_cells[cell])
                        if len(preys) > 0 and self.is_placement_in_cell_allowed(cell_idx=self.adjacent_cells[self.placements[agent_id]][cell], agent_id=agent_id):
                            return cell / 2
        return 4 # default: stay put
                    

    def pick_prey_direction(self, neighbourhood):
        predictions = self.model.predict(input_data=[neighbourhood])
        probabilites = predictions[0][0]
        probabilites[probabilites < 0] = 0
        probabilites = shelp.normalise(values=probabilites)
        if np.sum(probabilites) == 0: # in this case, all probabilities are 0 and thus it doesn't matter what we pick
            return np.random.choice(a=self.directions, size=1)
        return np.random.choice(a=self.directions, size=1, replace=True, p=probabilites)
    
    def get_cell_idx_for_direction(self, cell_idx, direction):
        x, y = sgrid.get_x_y_for_cell_idx(cell_idx=cell_idx, grid_size=self.grid_size)
        match direction:
            case 0: # up
                x = (x - 1) % self.grid_size[0] 
            case 1: # right
                y = (y + 1) % self.grid_size[1]
            case 2: # down
                x = (x + 1) % self.grid_size[0]
            case 3: # left
                y = (y - 1) % self.grid_size[1]
            case 4: # stay put
                pass 
        return sgrid.get_grid_cell_idx(x, y, self.grid_size)

    def make_moves(self, grid, placements, t):
        self.grid = copy.deepcopy(grid)
        self.placements = copy.deepcopy(placements)
        for agent in self.agents:
            cell_idx = self.placements[agent]
            if self.is_predator(agent_id=agent):
                direction = self.pick_predator_direction(agent_id=agent)
                if direction != 4:
                    self.last_predator_movements[agent] = t
                elif (t-self.last_predator_movements[agent]) > self.predator_random_movement_after:
                    direction = np.random.randint(0, 4)
                    self.last_predator_movements[agent] = t
            else:
                neighbourhood = self.get_neighbourhood(agent)
                direction = self.pick_prey_direction(neighbourhood=neighbourhood)
            new_cell_idx = self.get_cell_idx_for_direction(cell_idx=cell_idx, direction=direction)
            if new_cell_idx != cell_idx and self.is_placement_in_cell_allowed(cell_idx=new_cell_idx, agent_id=agent):
                placements[agent] = new_cell_idx
                grid[cell_idx].remove(agent)
                grid[new_cell_idx].append(agent)
        return grid, placements

    def simulate(self, tmax=1000):
        grid_history = []
        placements_history = []
        agents_history = []
        grid, placements = self.initialise_grid()
        for t in range(tmax):
            grid, placements = self.make_moves(grid, placements, t)
            self.grid = grid
            self.placements = placements
            self.eliminate_prey()
            grid_history.append(copy.deepcopy(self.grid))
            placements_history.append(copy.deepcopy(self.placements))
            agents_history.append(copy.deepcopy(self.agents))
            # print(f"t={t}/{tmax}")
            # self.print_grid()
        return agents_history, placements_history, grid_history

