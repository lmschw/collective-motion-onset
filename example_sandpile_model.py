from models.sandpile_model.sandpile_model import SandpileModel

from enums.placement_type import PlacementType
from enums.stress_introduction_type import StressIntroductionType

from animation.animator_matplotlib import MatplotlibAnimator
from animation.heatplot_animator import HeatplotAnimatorDensity, HeatplotAnimatorStress


tmax = 200
n = 20
grid_size = (5,5)

stress_threshold = 4

placement_type = PlacementType.RANDOM
stress_intro_type = StressIntroductionType.FLOAT_POS_NEG
num_stress_intro = 1
prob_stress_intro = None


simulator = SandpileModel(number_agents=n,
                          grid_size=grid_size,
                          placement_type=placement_type,
                          stress_threshold=stress_threshold,
                          stress_introduction_type=stress_intro_type,
                          num_stress_introduction=num_stress_intro,
                          probability_stress_introduction=prob_stress_intro)

simulation_data = simulator.simulate(tmax=tmax)
times, placements, densities, stress_levels = simulation_data

print(placements)
print(densities)
print(stress_levels)

model_params = {'n': n/2, 'domainSize': grid_size}

animation_filename_base = "test"

animation_filename = f"{animation_filename_base}_density"
animator = MatplotlibAnimator(simulation_data, (100,100,100))

# prepare the animator
preparedAnimator = animator.prepare(HeatplotAnimatorDensity(), frames=tmax)
preparedAnimator.setParams(model_params)


preparedAnimator.saveAnimation(f"{animation_filename}.mp4")

model_params = {'n': stress_threshold + 1, 'domainSize': grid_size}

animation_filename = f"{animation_filename_base}_stress"
animator = MatplotlibAnimator(simulation_data, (100,100,100))

# prepare the animator
preparedAnimator = animator.prepare(HeatplotAnimatorStress(), frames=tmax)
preparedAnimator.setParams(model_params)


preparedAnimator.saveAnimation(f"{animation_filename}.mp4")