import unittest
import numpy as np

import services.service_metrics as smet


class TestServiceMetrics(unittest.TestCase):
    def test_compute_longest_survival(self):
        survivals = [[False, False, False], [False, False, False], [False, False, False]]
        expected_timestep = -1
        assert expected_timestep == smet.compute_longest_survival(survivals=survivals)

        survivals = [[True, True, True], [False, False, False], [False, False, False]]
        expected_timestep = 0
        assert expected_timestep == smet.compute_longest_survival(survivals=survivals)

        survivals = [[True, True, False], [False, True, False], [False, False, False]]
        expected_timestep = 1
        assert expected_timestep == smet.compute_longest_survival(survivals=survivals)

        survivals = [[False, True, False], [False, True, False], [False, True, False]]
        expected_timestep = 2
        assert expected_timestep == smet.compute_longest_survival(survivals=survivals)

        survivals = [[True, True, True], [True, True, True], [True, True, True]]
        expected = 2
        assert expected == smet.compute_longest_survival(survivals=survivals)

    def test_compute_num_survivors_at_the_end(self):
        survivals = [[False, False, False], [False, False, False], [False, False, False]]
        expected = 0
        assert expected == smet.compute_num_survivors_at_the_end(survivals=survivals)

        survivals = [[True, True, True], [False, False, False], [False, False, False]]
        expected = 0
        assert expected == smet.compute_num_survivors_at_the_end(survivals=survivals)

        survivals = [[True, True, False], [False, True, False], [False, False, False]]
        expected = 0
        assert expected == smet.compute_num_survivors_at_the_end(survivals=survivals)

        survivals = [[False, True, False], [False, True, False], [False, True, False]]
        expected = 1
        assert expected == smet.compute_num_survivors_at_the_end(survivals=survivals)

        survivals = [[True, True, True], [True, True, True], [True, True, True]]
        expected = 3
        assert expected == smet.compute_num_survivors_at_the_end(survivals=survivals)

    def run_all(self):
        unittest.main(exit=False)
