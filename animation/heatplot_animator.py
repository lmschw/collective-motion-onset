import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import animation
from animation.animator import Animator
import numpy as np

class HeatplotAnimatorDensity(Animator):
    """
    Animator class for 2D graphical representation.
    """

    def setSimulationData(self, simulationData, domainSize, colours=None):
        """
        Sets
        keyword arguments:
        simulationData -- The simulation data array.
        domainSize -- The tuple that represents the lenghts of the square domain in each dimension.

        return:
        self
        """        
        self._time, _, self._positions, _ = simulationData
        self._domainSize = domainSize

        if colours is None:
            self._colours = len(self._time) * [len(self._positions) * ['k']]
        else:
            self._colours = colours

        return self
    
    def setParams(self, modelParams):
        self._n = modelParams["n"]
        self._domainSize = modelParams["domainSize"]

    def _animate(self, i):
        """
        Animator class that goes through sim data.

        keyword arguments:
        i -- Loop index.
        """

        plt.clf()
        sns.heatmap(self._positions[i,:,:], vmax=self._n)
        plt.title(f"Density: $t$={self._time[i]:.2f}")


class HeatplotAnimatorStress(Animator):
    """
    Animator class for 2D graphical representation.
    """

    def setSimulationData(self, simulationData, domainSize, colours=None):
        """
        Sets
        keyword arguments:
        simulationData -- The simulation data array.
        domainSize -- The tuple that represents the lenghts of the square domain in each dimension.

        return:
        self
        """        
        self._time, _, _, self._positions = simulationData
        self._domainSize = domainSize

        if colours is None:
            self._colours = len(self._time) * [len(self._positions) * ['k']]
        else:
            self._colours = colours

        return self
    
    def setParams(self, modelParams):
        self._n = modelParams["n"]
        self._domainSize = modelParams["domainSize"]

    def _animate(self, i):
        """
        Animator class that goes through sim data.

        keyword arguments:
        i -- Loop index.
        """

        plt.clf()
        sns.heatmap(self._positions[i,:, np.newaxis], vmax=self._n)
        plt.title(f"Stress: $t$={self._time[i]:.2f}")
