from simulate import WildFireSimulation
from make_plots import MakePlots
from visualize import Visualize
import numpy as np
from tqdm import tqdm
import os
import matplotlib.pyplot as plt

if __name__=="__main__":

    if not os.path.exists('plots'):
        os.makedirs('plots')
    
    # Example:
    rows = 100
    cols = 100
    n_simulations = 20
    
    sim = WildFireSimulation(rows, cols)
    
    # visualization = Visualize()
    
    # visualization.show_grid(sim)
    
    # visualization.animate(sim, steps=200) # with animation
    #visualization.plot_distribution(simulation)
    
    # burned = [WildFireSimulation.get_burnt(sim) for _ in range(n_simulations)]
    # plt.hist(burned)
    # plt.show()

    plotter = MakePlots(sim)

    # Define parameter and its range for sensitivity analysis
    # parameter = 'prob_delta_tree1'
    # values = [-0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4]

    # # Perform sensitivity analysis and plot
    # plotter.sensitivity_analysis(parameter, values)

    # perform sensitivity analysis for multiple parameters - TODO change params here
    parameters = ['prob_delta_tree1', 'prob_delta_dens1', 'wind_speed']
    values = [[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
              [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
              [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]]
    for i, parameter in enumerate(parameters):
        plotter.sensitivity_analysis(sim, parameter, values[i], n_simulations)
