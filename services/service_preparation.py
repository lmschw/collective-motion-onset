import numpy as np

def get_noise_amplitude_value_for_percentage(percentage):
    """
    Computes the noise amplitude for a given percentage.

    Params:
        - percentage (int, 1-100)

    Returns:
        The noise amplitude, a value in the range [0, 2pi]
    """
    if percentage < 0 or percentage > 100:
        raise Exception("Percentages must be between 0 and 100")
    return 2 * np.pi * (percentage/100)

def get_number_of_particles_for_constant_density_for_grid(density, grid_size, agents_per_cell_limit):
    """
    Computes the number of particles to keep the density constant for the supplied domain size.
    Density formula: "density" = "number of particles" / "domain area"

    Params:
        - density (float): the desired constant density of the domain
        - domain_size (tuple): tuple containing the x and y dimensions of the domain size

    Returns:
        The number of particles to be placed in the domain that corresponds to the density.
    """
    max_agents = grid_size[0] * grid_size[1] * agents_per_cell_limit
    return int(density * max_agents) # density * area

def get_density_for_grid(grid_size, number_of_particles, agents_per_cell_limit):
    """
    Computes the density of a given system.
    Density formula: "density" = "number of particles" / "domain area"

    Params:
        - domain_size (tuple): tuple containing the x and y dimensions of the domain size
        - number_particles (int): the number of particles to be placed in the domain

    Returns:
        The density of the system as a float.
    """
    max_agents = grid_size[0] * grid_size[1] * agents_per_cell_limit
    return number_of_particles / max_agents # n / area

def get_grid_size_for_constant_density(density, number_of_particles, agents_per_cell_limit):
    print(density, number_of_particles, agents_per_cell_limit)
    area = int(number_of_particles / (agents_per_cell_limit * density))
    factors = [[i, area//i] for i in range(1, int(area**0.5) + 1) if area % i == 0]
    return factors[-1]
