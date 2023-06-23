#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 13:15:01 2023

@author: gaston.barboza@goflink.com
"""

from simulate import WildFireSimulation
from visualize import Visualize
import numpy as np
import matplotlib.pyplot as plt

def run_simulations(n_simulations=100):
    burned_plot = []

    for _ in range(n_simulations):
        simulation = WildFireSimulation(rows, cols)
        simulation.run(steps)
        
        #count burned trees
        print(simulation.history[-1])
        burned_trees = np.count_nonzero(simulation.history[-1] == 4)
        burned_plot.append(burned_trees)

    plt.figure()
    plt.hist(burned_plot, bins='auto', edgecolor='black')

    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of burned_plot')

    plt.savefig('plots/simulation.png')
    # plt.show()

if __name__=="__main__":
    # Example:
    rows = 100
    cols = 100
    steps = 200
    
    simulation = WildFireSimulation(rows, cols)
    visualization = Visualize()
    
    visualization.show_grid(simulation)
    
    #simulation.run(steps) # without animation
    visualization.animate(simulation,100) # with animation
    visualization.plot_distribution(simulation)
    print(len(simulation.history))
    
    #run_simulations()