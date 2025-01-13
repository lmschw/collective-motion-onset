import unittest
import numpy as np

import services.service_saved_model as ssave

class TestServiceNeuralNetwork(unittest.TestCase):
    def test_save_and_load_model(self):
        model_params = {
            "n": 5,
            "grid_size": (3,3),
            "placement_type_prey": "RANDOM",
            "cell_visibility": "SQUARE_EIGHT",
            "allow_stay": True,
            "agents_per_cell_limit": 2,
            "num_predators": 1,
            "predator_behaviour": "NEAREST_PREY",
            "placement_type_predator": "RANDOM",
            "model_summary": "model_summary_test"
        }
        agents = [[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], [0, 2, 3, 4, 5], [0, 2, 3, 5], [0, 2, 3, 5], [0, 2, 5], [0, 2]]
        grids = [{0: [0], 1: [1], 2: [], 3: [4, 5], 4: [], 5: [], 6: [3], 7: [2], 8: []},
                 {0: [], 1: [0], 2: [1], 3: [4, 5], 4: [], 5: [], 6: [3], 7: [], 8: [2]},
                 {0: [], 1: [], 2: [0], 3: [4], 4: [5], 5: [], 6: [3], 7: [2], 8: []},
                 {0: [], 1: [], 2: [], 3: [0], 4: [], 5: [3, 5], 6: [], 7: [2], 8: []},
                 {0: [], 1: [], 2: [], 3: [], 4: [0], 5: [3], 6: [5], 7: [], 8: [2]},
                 {0: [], 1: [], 2: [], 3: [], 4: [], 5: [0], 6: [5], 7: [], 8: [2]},
                 {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [0], 7: [], 8: [2]}]
        placements = [{0: 0, 1: 1, 2: 7, 3: 6, 4: 3, 5: 3},
                      {0: 1, 1: 2, 2: 8, 3: 6, 4: 3, 5: 3},
                      {0: 2, 2: 7, 3: 6, 4: 3, 5: 4},
                      {0: 3, 2: 7, 3: 5, 5: 5},
                      {0: 4, 2: 8, 3: 5, 5: 6},
                      {0: 5, 2: 8, 5: 6},
                      {0: 6, 2: 8}]
        ssave.save_model(simulation_data=(agents, placements, grids), path="test.json", model_params=model_params, saveInterval=1)
        model_params_loaded, times, simulation_data_loaded = ssave.load_model(path="test.json")
        agents_loaded, placements_loaded, grids_loaded = simulation_data_loaded
        for k, v in model_params.items():
            assert v == model_params_loaded[k]
        for t in range(len(times)):
            for i in range(len(agents[t])):
                assert agents[t][i] == agents_loaded[t][i]
            for k, v in placements[t].items():
                assert v == placements_loaded[t][k]
            for k, v in grids[t].items():
                assert v == grids_loaded[t][k]
        ssave.delete_model(path="test.json")

        # test a different save interval
        ssave.save_model(simulation_data=(agents, placements, grids), path="test.json", model_params=model_params, saveInterval=3)
        model_params_loaded, times, simulation_data_loaded = ssave.load_model(path="test.json")
        assert len(times) == 3
        agents_loaded, placements_loaded, grids_loaded = simulation_data_loaded
        for k, v in model_params.items():
            assert v == model_params_loaded[k]
        for t in range(len(times)):
            for i in range(len(agents[t])):
                assert agents[t][i] == agents_loaded[t][i]
            for k, v in placements[t].items():
                assert v == placements_loaded[t][k]
            for k, v in grids[t].items():
                assert v == grids_loaded[t][k]
        ssave.delete_model(path="test.json")

    def run_all(self):
        unittest.main(exit=False)
