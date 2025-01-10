import numpy as np
from simulators.sandpile_model.sandpile_model_movement import SandpileModel
from enums.placement_type import PlacementTypePredator, PlacementTypePrey
from enums.cell_visibility import CellVisibility
from enums.predator_behaviour import PredatorBehaviour
from neural_network.neural_network import NeuralNetwork
from neural_network.activation_layer import ActivationLayer
from neural_network.fully_connected_layer import FullyConnectedLayer
import services.service_neural_network as snn
import services.service_preparation as sprep
from animation.animator import Animator
from animation.animator_matplotlib import MatplotlibAnimator
from animation.grid_animator import GridAnimator

weights = np.array([0.78923, 0.,      0,      0.,      0,      0.02552, 1.,      0.     ])
weights = np.array([0.0,0.15977112926290582,0.0,0.24335885406420038,0.44701763141229406,0.12221490128966903,0.0,0.02763748397093066])
weights = np.array([0.011230748208120903,0.43914108664312007,0.0,0.5301038600277325,0.0,0.019524305121026497,0.0,0.0])

tmax = 1000
grid_size = (5,5)
density = 0.3
num_particles = None
num_generations = 20
num_iters = 1
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

if num_particles == None:
    num_particles = sprep.get_number_of_particles_for_constant_density_for_grid(density=density, grid_size=grid_size, agents_per_cell_limit=agent_per_cell_limit)


weights_size = 8
nn = NeuralNetwork()
fully_connected_layer = FullyConnectedLayer(input_size=weights_size, output_size=5)
fully_connected_layer.set_weights(weights=weights)
nn.add(fully_connected_layer)
nn.add(ActivationLayer(activation=snn.tanh, activation_prime=snn.tanh_prime))

for i in range(20):
    model = SandpileModel(
                                            num_agents=num_particles,
                                            grid_size=grid_size,
                                            model=nn,
                                            placement_type_prey=placemenent_prey,
                                            cell_visibility=cell_visibility,
                                            allow_stay=allow_stay,
                                            agents_per_cell_limit=agent_per_cell_limit,
                                            num_predators=num_predator,
                                            predator_behaviour=PredatorBehaviour.NEAREST_PREY,
                                            placement_type_predator=placement_predator,
    )
    simulation_data = model.simulate(tmax=tmax)

    animation_filename_base = f"test_{i}"

    animation_filename = f"{animation_filename_base}"
    animator = MatplotlibAnimator(simulation_data, (grid_size[0],grid_size[1],100))
    preparedAnimator = animator.prepare(GridAnimator(), frames=tmax)
    preparedAnimator.setSimulationData(simulation_data=simulation_data, grid_size=grid_size, num_predators=num_predator)
    preparedAnimator.saveAnimation(f"{animation_filename}.mp4")