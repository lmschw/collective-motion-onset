import numpy as np
from evolution.differential_evolution_sandpile_movement import DifferentialEvolution
from simulators.sandpile_model.sandpile_model_movement import SandpileModel
from enums.placement_type import PlacementTypePredator, PlacementTypePrey
from enums.cell_visibility import CellVisibility
from enums.predator_behaviour import PredatorBehaviour

evo = DifferentialEvolution(tmax=100,
                            grid_size=(5, 5),
                            density=None,
                            num_particles=15,
                            num_generations=20,
                            num_iterations_per_individual=1,
                            use_norm=True,
                            population_size=30,
                            bounds=[0,1],
                            update_to_zero_bounds=[0,0],
                            mutation_scale_factor=1,
                            crossover_rate=0.5,
                            early_stopping_after_gens=None,
                            cell_visibility=CellVisibility.SQUARE_EIGHT,
                            allow_stay=True,
                            agents_per_cell_limit=2,
                            placement_type_prey=PlacementTypePrey.RANDOM,
                            placement_type_predator=PlacementTypePredator.RANDOM)

evo.run(save_path_plots="test_plots.jpeg", save_path_log="test_log.csv")
