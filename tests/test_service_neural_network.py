import unittest
import numpy as np

import services.service_neural_network as snn

class TestServiceNeuralNetwork(unittest.TestCase):
    def test_tanh(self):
        values = [0, np.pi, 2*np.pi]
        expected = [0, 0.9963, 1]
        for i in range(len(values)):
            assert np.absolute(expected[i] - snn.tanh(x=values[i])) <= 0.0001

    def test_tanh_prime(self):
        values = [0, np.pi, 2*np.pi]
        expected = [1, 0.00738, 0]
        for i in range(len(values)):
            assert np.absolute(expected[i] - snn.tanh_prime(x=values[i])) <= 0.0001

    def test_mse(self):
        y_trues = [0, 0.5, 1]
        y_preds = [0.1, 0.4, 1]
        expected = [0.1, 0.1, 0]
        for i in range(len(y_trues)):
            assert np.absolute(expected[i] - snn.mse(y_pred=y_preds[i], y_true=y_trues[i])) <= 0.0001

    def test_mse(self):
        y_trues = [0, 0.5, 1]
        y_preds = [0.1, 0.4, 1]
        expected = [0.01, 0.01, 0]
        for i in range(len(y_trues)):
            assert np.absolute(expected[i] - snn.mse(y_pred=y_preds[i], y_true=y_trues[i])) <= 0.0001

    def test_mse_prime(self):
        y_trues = [np.array([0]), np.array([0.5]), np.array([1])]
        y_preds = [np.array([0.1]), np.array([0.4]), np.array([1])]
        expected = [0.2, -0.2, 0]
        for i in range(len(y_trues)):
            assert np.absolute(expected[i] - snn.mse_prime(y_pred=y_preds[i], y_true=y_trues[i])[0]) <= 0.0001

    def run_all(self):
        unittest.main(exit=False)
