from simulators.sandpile_model.sandpile_model_movement import SandpileModel
from enums.placement_type import PlacementTypePredator, PlacementTypePrey
from enums.cell_visibility import CellVisibility
from enums.predator_behaviour import PredatorBehaviour

model = SandpileModel(num_agents=5,
                      grid_size=(5,5),
                      model=None,
                      placement_type_prey=PlacementTypePrey.RANDOM,
                      cell_visibility=CellVisibility.SQUARE_EIGHT,
                      num_directions=4,
                      allow_stay=True,
                      agents_per_cell_limit=2,
                      num_predators=1,
                      predator_behaviour=PredatorBehaviour.NEAREST_PREY,
                      placement_type_predator=PlacementTypePredator.BORDER)

model.print_grid()