import unittest
import numpy as np

from neural_network.neural_network import NeuralNetwork
from neural_network.fully_connected_layer import FullyConnectedLayer
from neural_network.activation_layer import ActivationLayer
import services.service_neural_network as snn

class TestNeuralNetwork(unittest.TestCase):

    def test_xor(self):
        x_train = np.array([[[0,0]], [[0,1]], [[1,0]], [[1,1]]])
        y_train = np.array([[[0]], [[1]], [[1]], [[0]]])

        net = NeuralNetwork()
        net.add(FullyConnectedLayer(2, 3))
        net.add(ActivationLayer(snn.tanh, snn.tanh_prime))
        net.add(FullyConnectedLayer(3, 1))
        net.add(ActivationLayer(snn.tanh, snn.tanh_prime))

        net.use(snn.mse, snn.mse_prime)
        net.fit(x_train, y_train, epochs=1000, learning_rate=0.1)

        out = net.predict(x_train)
        # the results would ideally be as close to 0, 1, 1, 0 as possible 
        # but we cannot be sure due to the training so we just test if they fall 
        # on the right side of 0.5
        assert out[0][0][0] <= 0.5
        assert out[1][0][0] >= 0.5
        assert out[2][0][0] >= 0.5
        assert out[3][0][0] <= 0.5

    def test_summary(self):
        net = NeuralNetwork()
        fc = FullyConnectedLayer(2,3)
        fc.set_weights([0.4, 0.6])
        net.add(fc)
        net.add(ActivationLayer(snn.tanh, snn.tanh_prime))

        expected_summary = f"NN_FC_b={fc.bias}_w=0.4,0.6_A_a=tanh_ap=tanh_prime"

        assert expected_summary == net.get_model_summary()

    def run_all(self):
        unittest.main(exit=False)