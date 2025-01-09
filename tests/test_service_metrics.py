import unittest
import numpy as np

import services.service_metrics as smet


class TestServiceMetrics(unittest.TestCase):
    def test_compute_longest_survival(self):
        num_predators = 1
        agents = [[], [], []]
        expected_timestep = -1
        assert expected_timestep == smet.compute_longest_survival(agents=agents, num_predators=num_predators)

        agents = [[1, 2, 3], [], []]
        expected_timestep = 0
        assert expected_timestep == smet.compute_longest_survival(agents=agents, num_predators=num_predators)

        agents = [[1, 2], [2], []]
        expected_timestep = 1
        assert expected_timestep == smet.compute_longest_survival(agents=agents, num_predators=num_predators)

        agents = [[2], [2], [2]]
        expected_timestep = 2
        assert expected_timestep == smet.compute_longest_survival(agents=agents, num_predators=num_predators)

        agents = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        expected = 2
        assert expected == smet.compute_longest_survival(agents=agents, num_predators=num_predators)

    def test_compute_num_survivors_at_the_end(self):
        num_predators = 1
        agents = [[], [], []]
        expected = 0
        assert expected == smet.compute_num_survivors_at_the_end(agents=agents, num_predators=num_predators)

        agents = [[1, 2, 3], [], []]
        expected = 0
        assert expected == smet.compute_num_survivors_at_the_end(agents=agents, num_predators=num_predators)

        agents = [[1, 2], [2], []]
        expected = 0
        assert expected == smet.compute_num_survivors_at_the_end(agents=agents, num_predators=num_predators)

        agents = [[2], [2], [2]]
        expected = 1
        assert expected == smet.compute_num_survivors_at_the_end(agents=agents, num_predators=num_predators)

        agents = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        expected = 3
        assert expected == smet.compute_num_survivors_at_the_end(agents=agents, num_predators=num_predators)

    def run_all(self):
        unittest.main(exit=False)
