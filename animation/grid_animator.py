import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from animation.animator import Animator
import services.service_grid as sgrid

class GridAnimator(Animator):
    def setSimulationData(self, simulation_data, grid_size, num_predators=1, colours=None):
        """
        Sets
        keyword arguments:
        simulationData -- The simulation data array.
        domainSize -- The tuple that represents the lenghts of the square domain in each dimension.

        return:
        self
        """        
        self.agents, self.placements, self.grid = simulation_data
        self._time = np.array([i for i in range(len(self.agents))])
        self._domainSize = grid_size
        self.num_predators = num_predators

        self._colours = colours

        return self
    
    def _animate(self, t):
        """
        Animator class that goes through sim data.

        keyword arguments:
        i -- Loop index.
        """
        if t % 1000 == 0:
            print(t)

        plt.clf()
        points = np.zeros((len(self.agents[t]), 2))
        colours = np.full(len(self.agents[t]), 'b')
        for i, agent in enumerate(self.agents[t]):
            if agent < self.num_predators:
                colours[i] = 'r'
            x, y = sgrid.get_x_y_for_cell_idx(self.placements[t][agent], self._domainSize)
            points[i][0] = x
            points[i][1] = y
        #plt.plot(points[:,0],points[:,1],'ro')
        #print(points)
        plt.scatter(points[:,0], points[:,1], c=colours)
        plt.title(f"$t$={t:.2f}")
