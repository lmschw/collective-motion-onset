import numpy as np
from evolution.differential_evolution_sandpile_movement import DifferentialEvolution
from simulators.sandpile_model.sandpile_model_movement import SandpileModel
from enums.placement_type import PlacementTypePredator, PlacementTypePrey
from enums.cell_visibility import CellVisibility
from enums.predator_behaviour import PredatorBehaviour
from enums.metrics import Metrics
import services.service_logging as slog
import services.service_helper as shelp

tmax = 1000
grid_size = (25,25)
num_particles = None
num_generations = 20
num_ind_iters = 10
num_iters = 50
population_size = 30
bounds = [0,1]
zero_bounds = [0,0]
cell_visibility = CellVisibility.SQUARE_EIGHT
allow_stay = True
early_stopping = None
agent_per_cell_limit = 2
placemenent_prey = PlacementTypePrey.RANDOM
placement_predator = PlacementTypePredator.RANDOM
num_predator = 1
predator_random_movement_after = 50
metric = Metrics.NUMBER_OF_SURVIVORS_AT_FINAL_TIMESTEP

for num_predator in [1, 2, 3]:
    for agent_per_cell_limit in [2, 1, 3]:
        for density in [0.3, 0.2, 0.4, 0.1, 0.5, 0.6]:
            for grid_size in [(5, 5), (10, 10), (25, 25), (100, 100)]:
                postfix = f"_test_tmax={tmax}_grid={grid_size}_d={density}_n={num_particles}_cv={cell_visibility.value}_as={allow_stay}_lim={agent_per_cell_limit}_plp={placemenent_prey.value}_plh={placement_predator.value}_m={metric.value}"
                save_path_best = f"best{postfix}.csv"
                save_path_best_normalised = f"best{postfix}_normalised.csv"
                save_path_general = f"all{postfix}"
                save_path_plot = f"plot{postfix}"

                slog.initialise_log_file_with_headers(slog.create_headers(len_weights=cell_visibility.number_cells, is_best=True), save_path=save_path_best)
                slog.initialise_log_file_with_headers(slog.create_headers(len_weights=cell_visibility.number_cells, is_best=True), save_path=save_path_best_normalised)

                for i in range(num_iters):
                    evo = DifferentialEvolution(tmax=tmax,
                                            grid_size=grid_size,
                                            density=density,
                                            num_particles=num_particles,
                                            num_generations=num_generations,
                                            num_iterations_per_individual=num_ind_iters,
                                            use_norm=True,
                                            population_size=population_size,
                                            bounds=bounds,
                                            update_to_zero_bounds=zero_bounds,
                                            early_stopping_after_gens=early_stopping,
                                            cell_visibility=cell_visibility,
                                            allow_stay=allow_stay,
                                            agents_per_cell_limit=agent_per_cell_limit,
                                            placement_type_prey=placemenent_prey,
                                            placement_type_predator=placement_predator,
                                            num_predators=num_predator,
                                            predator_random_movement_after=predator_random_movement_after,
                                            metric=metric)

                    
                    best = evo.run(save_path_log=save_path_general, save_path_plots=save_path_plot)
                    print(f"BEST overall: {best}")


                    slog.log_results_to_csv([{'iter': i, 'individual': np.array(best[0]), 'fitness': best[1]}], prepare=True, save_path=save_path_best)
                    slog.log_results_to_csv([{'iter': i, 'individual': shelp.normalise(np.array(best[0])), 'fitness': best[1]}], prepare=True, save_path=save_path_best_normalised)

