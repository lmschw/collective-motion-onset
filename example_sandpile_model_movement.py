import numpy as np
from simulators.sandpile_model.sandpile_model_movement import SandpileModel
from enums.placement_type import PlacementTypePredator, PlacementTypePrey
from enums.cell_visibility import CellVisibility
from enums.predator_behaviour import PredatorBehaviour
from neural_network.neural_network import NeuralNetwork
from neural_network.activation_layer import ActivationLayer
from neural_network.fully_connected_layer import FullyConnectedLayer
import services.service_neural_network as snn

weights_size = 8
weights = np.array([0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0.1, 0.2])
nn = NeuralNetwork()
fully_connected_layer = FullyConnectedLayer(input_size=weights_size, output_size=5)
fully_connected_layer.set_weights(weights=weights)
nn.add(fully_connected_layer)
nn.add(ActivationLayer(activation=snn.tanh, activation_prime=snn.tanh_prime))

model = SandpileModel(num_agents=5,
                      grid_size=(5,5),
                      model=nn,
                      placement_type_prey=PlacementTypePrey.RANDOM,
                      cell_visibility=CellVisibility.SQUARE_EIGHT,
                      allow_stay=True,
                      agents_per_cell_limit=2,
                      num_predators=1,
                      predator_behaviour=PredatorBehaviour.NEAREST_PREY,
                      placement_type_predator=PlacementTypePredator.BORDER)

model.print_grid()
model.simulate(tmax=5)