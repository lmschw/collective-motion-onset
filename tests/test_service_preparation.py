import unittest
import numpy as np

import services.service_preparation as sprep


class TestServicePreparation(unittest.TestCase):
    def test_get_noise_amplitude_value_for_percentage(self):
        valid_percentages = [0, 1, 50, 100]
        expected_valid_noises = [0, 0.06283, 3.14159, 6.28318]
        for i in range(len(valid_percentages)):
            assert expected_valid_noises[i] - np.absolute(sprep.get_noise_amplitude_value_for_percentage(valid_percentages[i])) <= 0.0001
        invalid_percentages = [-1, 101]
        for percentage in invalid_percentages:
            self.assertRaises(Exception, sprep.get_noise_amplitude_value_for_percentage, self, percentage)

    def test_get_number_of_particles_for_constant_density_for_grid(self):
        grid_size_squared = (5, 5)
        grid_size_more_rows = (5, 4)
        grid_size_more_cols = (4, 5)
        agents_per_cell_limits = [1, 2, 3]
        densities = [0.1, 0.25, 0.5, 1]
        expected_squared = [[2, 5, 7], [6, 12, 18], [12, 25, 37], [25, 50, 75]]
        expected_more_rows = [[2, 4, 6], [5, 10, 15], [10, 20, 30], [20, 40, 60]]
        expected_more_cols = [[2, 4, 6], [5, 10, 15], [10, 20, 30], [20, 40, 60]]

        for i in range(len(densities)):
            for j in range(len(agents_per_cell_limits)):
                assert expected_squared[i][j] == sprep.get_number_of_particles_for_constant_density_for_grid(density=densities[i], grid_size=grid_size_squared, agents_per_cell_limit=agents_per_cell_limits[j])
                assert expected_more_rows[i][j] == sprep.get_number_of_particles_for_constant_density_for_grid(density=densities[i], grid_size=grid_size_more_rows, agents_per_cell_limit=agents_per_cell_limits[j])
                assert expected_more_cols[i][j] == sprep.get_number_of_particles_for_constant_density_for_grid(density=densities[i], grid_size=grid_size_more_cols, agents_per_cell_limit=agents_per_cell_limits[j])

    def test_get_density_for_grid(self):
        grid_size_squared = (5, 5)
        grid_size_more_rows = (5, 4)
        grid_size_more_cols = (4, 5)
        agents_per_cell_limits = [1, 2, 3]
        agents_squared = [1, 5, 10, 25]
        agents_non_squared = [1, 5, 10, 20]
        expected_squared = [[0.04, 0.02, 0.013], [0.2, 0.1, 0.067], [0.4, 0.2, 0.133], [1, 0.5, 0.333]]
        expected_non_squared = [[0.05, 0.025, 0.017], [0.25, 0.125, 0.083], [0.5, 0.25, 0.167], [1, 0.5, 0.333]]

        for i in range(len(agents_squared)):
            for j in range(len(agents_per_cell_limits)):
                assert np.absolute(expected_squared[i][j] - sprep.get_density_for_grid(grid_size=grid_size_squared, number_of_particles=agents_squared[i], agents_per_cell_limit=agents_per_cell_limits[j])) < 0.001

        for i in range(len(agents_non_squared)):
            for j in range(len(agents_per_cell_limits)):
                assert np.absolute(expected_non_squared[i][j] - sprep.get_density_for_grid(grid_size=grid_size_more_rows, number_of_particles=agents_non_squared[i], agents_per_cell_limit=agents_per_cell_limits[j])) < 0.001
                assert np.absolute(expected_non_squared[i][j] - sprep.get_density_for_grid(grid_size=grid_size_more_cols, number_of_particles=agents_non_squared[i], agents_per_cell_limit=agents_per_cell_limits[j])) < 0.001

    def test_get_grid_size_for_constant_density(self):
        densities = [0.1, 0.5, 1]
        num_agents = [10, 50]
        limits = [1, 2]
        for i in range(len(densities)):
            for j in range(len(num_agents)):
                for k in range(len(limits)):
                    result = sprep.get_grid_size_for_constant_density(density=densities[i], number_of_particles=num_agents[j], agents_per_cell_limit=limits[k])
                    assert num_agents[j] == sprep.get_number_of_particles_for_constant_density_for_grid(density=densities[i], grid_size=result, agents_per_cell_limit=limits[k])

    def run_all(self):
        unittest.main(exit=False)
