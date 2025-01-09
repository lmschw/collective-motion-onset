import numpy as np
import scipy.integrate as integrate
import csv
import matplotlib.pyplot as plt

from neural_network.activation_layer import ActivationLayer
from neural_network.fully_connected_layer import FullyConnectedLayer
from neural_network.neural_network import NeuralNetwork
import services.service_helper as shelp
import services.service_logging as slog
import services.service_metrics as smet
import services.service_neural_network as snn
import services.service_preparation as sprep
from simulators.sandpile_model.sandpile_model_movement import SandpileModel

from enums.cell_visibility import CellVisibility
from enums.metrics import Metrics
from enums.predator_behaviour import PredatorBehaviour
from enums.placement_type import PlacementTypePrey, PlacementTypePredator


class DifferentialEvolution:
    def __init__(self, tmax, grid_size=(None, None), density=None, num_particles=None, 
                 num_generations=1000, num_iterations_per_individual=1, use_norm=True, 
                 population_size=100, bounds=[0, 1], update_to_zero_bounds=[0,0], mutation_scale_factor=1, 
                 crossover_rate=0.5, early_stopping_after_gens=None, cell_visibility=CellVisibility.SQUARE_EIGHT, 
                 allow_stay=True, agents_per_cell_limit=2, placement_type_prey=PlacementTypePrey.RANDOM, 
                 placement_type_predator=PlacementTypePredator.RANDOM, num_predators=1, 
                 predator_behaviour=PredatorBehaviour.NEAREST_PREY, metric=Metrics.NUMBER_OF_SURVIVORS_AT_FINAL_TIMESTEP):
        """
        Models the DE approach.

        Params:
            - radius (int): the perception radius of the particles
            - tmax (int): the number of timesteps for each simulation
            - grid_size (tuple of floats) [optional]: the dimensions of the domain
            - density (float) [optional]: the density of the particles within the domain
            - num_particles (int) [optional]: how many particles are within the domain
            - speed (float) [optional, default=1]: how fast the particles move
            - noise_percentage (float) [optional, default=0]: how much environmental noise is present in the domain
            - num_generations (int) [optional, default=1000]: how many generations are generated and validated
            - num_iterations_per_individual (int) [optional, default=10]: how many times the simulation is run for every individual
            - add_own_orientation (boolean) [optional, default=False]: should the particle's own orientation be considered (added to weights and orientations)
            - add_random (boolean) [optional, default=False]: should a random value be considered (added to weights and orientations). Orientation value generated randomly at every timestep
            - start_timestep_evaluation (int) [optional, default=0]: the first timestep for which the difference between expected and actual result should be computed
            - changeover_point_timestep (int) [optional, default=0]: if we expect a change in the order, this indicated the timestep for that change
            - start_order (int: 0 or 1) [optional]: the order at the start. If this is not set, half the simulation runs are started with an ordered starting condition and half with a disordered starting condition
            - target_order (int: 0 or 1) [optional, default=1]: the expected order at the end
            - population_size (int) [optional, default=100]: how many individuals are generated per generation
            - bounds (list of 2 ints) [optional, default=[-1, 1]]: the bounds for the c_value generation
        """

        self.num_generations = num_generations
        self.num_iterations_per_individual = num_iterations_per_individual

        self.tmax = tmax
        self.use_norm = use_norm
        self.population_size = population_size
        self.bounds = bounds
        self.update_to_zero_bounds = update_to_zero_bounds
        self.mutation_scale_factor = mutation_scale_factor
        self.crossover_rate = crossover_rate
        self.early_stopping_after_gens = early_stopping_after_gens

        self.cell_visibility = cell_visibility
        self.allow_stay = allow_stay
        self.agents_per_cell_limit = agents_per_cell_limit
        self.placement_type_prey = placement_type_prey
        self.placement_type_predator = placement_type_predator
        self.num_predators = num_predators
        self.predator_behaviour = predator_behaviour
        self.metric = metric

        if any(ele is None for ele in grid_size) and (density == None or num_particles == None):
            raise Exception("If you do not suppy a grid_size, you need to provide both the density and the number of particles.")
        elif density == None and num_particles == None:
            raise Exception("Please supply either the density or the number of particles.")
        elif density != None and not any(ele is None for ele in grid_size):
            self.density = density
            self.grid_size = grid_size
            self.num_particles = sprep.get_number_of_particles_for_constant_density_for_grid(self.density, self.grid_size, self.agents_per_cell_limit)
        elif num_particles and not any(ele is None for ele in grid_size):
            self.num_particles = num_particles
            self.grid_size = grid_size
            self.density = sprep.get_density_for_grid(self.grid_size, self.num_particles, self.agents_per_cell_limit)
        else:
            self.density = density
            self.num_particles = num_particles
            self.grid_size = sprep.get_grid_size_for_constant_density(self.density, self.num_particles, self.agents_per_cell_limit)

        # TODO add enum to include other options
        self.c_value_size = self.cell_visibility.number_cells
        self.directions = 4
        if self.allow_stay:
            self.directions += 1

        print(f"dom={self.grid_size}, d={self.density}, n={self.num_particles}")

    def create_initial_population(self):
        return np.random.uniform(low=self.bounds[0], high=self.bounds[1], size=((self.population_size, self.c_value_size)))

    def create_neural_network(self, weights):
        nn = NeuralNetwork()
        fully_connected_layer = FullyConnectedLayer(input_size=self.c_value_size, output_size=self.directions)
        fully_connected_layer.set_weights(weights=weights)
        nn.add(fully_connected_layer)
        nn.add(ActivationLayer(activation=snn.tanh, activation_prime=snn.tanh_prime))
        return nn

    def evaluate_results(self, agents):
        match self.metric:
            case Metrics.LONGEST_SURVIVAL:
                return (self.tmax - smet.compute_longest_survival(agents=agents, num_predators=self.num_predators)) / self.tmax
            case Metrics.NUMBER_OF_SURVIVORS_AT_FINAL_TIMESTEP:
                return (self.num_particles - smet.compute_num_survivors_at_the_end(agents=agents, num_predators=self.num_predators)) / self.num_particles

    def fitness_function(self, weights):
        results = []
        weights = self.update_weights(weights)
        model = self.create_neural_network(weights=weights)
        for i in range(self.num_iterations_per_individual):
            simulator = SandpileModel(
                                        num_agents=self.num_particles,
                                        grid_size=self.grid_size,
                                        model=model,
                                        placement_type_prey=self.placement_type_prey,
                                        cell_visibility=self.cell_visibility,
                                        allow_stay=self.allow_stay,
                                        agents_per_cell_limit=self.agents_per_cell_limit,
                                        num_predators=self.num_predators,
                                        predator_behaviour=self.predator_behaviour,
                                        placement_type_predator=self.placement_type_predator,
                                    )
            agents, placements, grid = simulator.simulate(tmax=self.tmax)
            results.append(self.evaluate_results(agents=agents))
        fitness = np.average(results)
        return fitness
    
    def mutation(self, x, F):
        return x[0] + F * (x[1] - x[2])
    
    def check_bounds(self, mutated, bounds):
        mutated_bound = np.clip(mutated, bounds[0], bounds[1])
        return mutated_bound
    
    def crossover(self, mutated, target, cr):
        # generate a uniform random value for every dimension
        p = np.random.rand(self.c_value_size)
        # generate trial vector by binomial crossover
        trial = [mutated[i] if p[i] < cr else target[i] for i in range(self.c_value_size)]
        return np.array(trial)
    
    def update_weights(self, weights):
        weights = np.where(((weights >= self.update_to_zero_bounds[0]) & (weights <= self.update_to_zero_bounds[1])), 0, weights)
        if self.use_norm == True:
            weights = shelp.normalise(weights, norm='l1')
        return weights
    
    def plot_fitnesses(self, fitnesses, save_path_plots=None):
        plt.plot(fitnesses)
        if save_path_plots:
            plt.savefig(f"{save_path_plots}.svg")
            plt.savefig(f"{save_path_plots}.jpeg")
        else:
            plt.show()         

    def run(self, save_path_plots=None, save_path_log=None, log_depth='all'):
        with open(f"{save_path_log}.csv", 'a', newline='') as log:
            w = csv.writer(log)
            headers = slog.create_headers(self.c_value_size)
            w.writerow(headers)
            log.flush()
            population  = self.create_initial_population()
            fitnesses = [self.fitness_function(individual) for individual in population]
            best_individual = population[np.argmin(fitnesses)]
            best_fitness = min(fitnesses)
            prev_fitness = best_fitness
            best_fitnesses_for_generations = [best_fitness]
            # saving the fitnesses
            if log_depth == 'all':
                log_dict_list = slog.create_dicts_for_logging(-1, population, fitnesses)
            else:
                log_dict_list = slog.create_dicts_for_logging(-1, [best_individual], [best_fitness])
            for dict in log_dict_list:
                w.writerow(dict.values())
            log.flush()
            last_improvement_at_gen = 0
            for iter in range(self.num_generations):
                print(f"gen {iter+1}/{self.num_generations}")
                for ind in range(self.population_size):
                    candidates = [candidate for candidate in range(self.population_size) if candidate != ind]
                    a, b, c = population[np.random.choice(candidates, 3, replace=False)]
                    mutated = self.mutation([a, b, c], self.mutation_scale_factor)
                    mutated = self.check_bounds(mutated, self.bounds)
                    trial = self.crossover(mutated, population[ind], self.crossover_rate)
                    target_existing = fitnesses[ind]
                    target_trial = self.fitness_function(trial)
                    if target_trial < target_existing:
                        population[ind] = trial
                        fitnesses[ind] = target_trial
                best_fitness = min(fitnesses)
                if best_fitness < prev_fitness:
                    best_individual = population[np.argmin(fitnesses)]
                    prev_fitness = best_fitness
                    last_improvement_at_gen = iter
                    print('Iteration: %d f([%s]) = %.5f' % (iter, np.around(best_individual, decimals=5), best_fitness))
                # saving the fitnesses
                if log_depth == 'all':
                    log_dict_list = slog.create_dicts_for_logging(iter, population, fitnesses)
                else:
                    log_dict_list = slog.create_dicts_for_logging(iter, [best_individual], [best_fitness])
                for dict in log_dict_list:
                    w.writerow(dict.values())
                log.flush()
                best_fitnesses_for_generations.append(best_fitness)
                if self.early_stopping_after_gens != None and iter-last_improvement_at_gen > self.early_stopping_after_gens:
                    print(f"Early stopping at iteration {iter} after {self.early_stopping_after_gens} generations without improvement")
                    break

            self.plot_fitnesses(best_fitnesses_for_generations, save_path_plots)
            return [best_individual, best_fitness]
