#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 13:14:12 2023

@author: gaston.barboza@goflink.com
"""
import copy
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import animation as animation
import numpy as np

class Visualize():
    def __init__(self):
        pass
    
    def animate(self,sim, steps):
        animations = []
        fig = plt.figure()
        for _ in range(steps):
            # update_grid()
            new_grid = copy.deepcopy(sim.update_grid())
            grid_arr = np.array(new_grid)

            # visualize
            ani = plt.imshow(grid_arr, animated=True, interpolation="none", cmap=cm.viridis)
            animations.append([ani])
            
        gif = animation.ArtistAnimation(fig, animations, interval=100, blit=True,repeat_delay=100)
        gif.save('plots/gif-tree-type.gif')
        plt.show()

    
    def plot_distribution(self,sim):
        plot_empty = []
        plot_trees = []
        plot_burning = []
        plot_burned = []

        for state in sim.history:
            num_empty = np.count_nonzero(state == 1) #TODO empty may be removed
            num_trees = np.count_nonzero(state == 2) 
            num_burning = np.count_nonzero(state == 3)
            num_burned = np.count_nonzero(state == 4)

            plot_empty.append(num_empty)
            plot_trees.append(num_trees)
            plot_burning.append(num_burning)
            plot_burned.append(num_burned)

        time_steps = range(len(plot_empty))

        plt.figure()
        plt.plot(time_steps, plot_empty, label='Empty')
        plt.plot(time_steps, plot_trees, label='Trees')
        plt.plot(time_steps, plot_burning, label='Burning')
        plt.plot(time_steps, plot_burned, label='Burned')
        plt.xlabel('Time Step')
        plt.ylabel('Number of Cells')
        plt.title('Distribution of Cells over Time')
        plt.legend()
        plt.savefig('plots/plot_empty.png')