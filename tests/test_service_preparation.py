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

    def run_all(self):
        unittest.main(exit=False)
