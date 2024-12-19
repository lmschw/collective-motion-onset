import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import animation
from animation.animator import Animator
import numpy as np

class HeatplotAnimator(Animator):
    def setSimulationData(self, simulationData, domainSize, colours=None):
        """
        Sets
        keyword arguments:
        simulationData -- The simulation data array.
        domainSize -- The tuple that represents the lenghts of the square domain in each dimension.

        return:
        self
        """        
        self._time, self.placements, self.densities, self.stress_levels = simulationData
        self.pick_positions()
        self._domainSize = domainSize

        if colours is None:
            self._colours = len(self._time) * [len(self._positions) * ['k']]
        else:
            self._colours = colours

        return self
    
    def setParams(self, modelParams):
        self._n = modelParams["n"]
        self._domainSize = modelParams["domainSize"]

    def pick_positions(self):
        pass

    def base_title(self):
        pass

    def get_heatmap_data(self, i):
        return self._positions[i,:,:]

    def _leaving_string(self, t):
        new_count = 0
        for i in range(len(self.placements[t])):
            if self.placements[t][i] < 0 :
                if (t==0 or self.placements[t-1][i] >= 0):
                    new_count += 1
        unique, counts = np.unique(self.placements[t], return_counts=True)
        cts = dict(zip(unique, counts))
        leaving_str = f"left from: "
        for k, v in cts.items():
            if k < 0:
                leaving_str += f"{int(-k)}: {v}, "
        leaving_str += f"new leavers: {new_count}"
        return leaving_str
    
    def _animate(self, i):
        """
        Animator class that goes through sim data.

        keyword arguments:
        i -- Loop index.
        """
        plt.clf()
        sns.heatmap(self.get_heatmap_data(i), vmax=self._n)
        plt.title(f"{self.base_title()} $t$={self._time[i]:.2f}\n {self._leaving_string(i)}")


class HeatplotAnimatorDensity(HeatplotAnimator):
    """
    Animator class for 2D graphical representation.
    """
    def pick_positions(self):
        self._positions = self.densities

    def base_title(self):
        return 'Density:'


class HeatplotAnimatorStress(HeatplotAnimator):
    """
    Animator class for 2D graphical representation.
    """
    def pick_positions(self):
        self._positions = self.stress_levels

    def base_title(self):
        return 'Stress:'
    
    def get_heatmap_data(self, i):
        return self._positions[i,:,np.newaxis]