from simulate import WildFireSimulation
from make_plots import MakePlots
from visualize import Visualize
import os
import matplotlib.pyplot as plt
import numpy as np

def get_burnt(sim):
    sim.run()
    percentage = sim.burned_trees/sim.total_trees
    sim.reset()
    return percentage

if __name__=="__main__":

    if not os.path.exists('plots'):
        os.makedirs('plots')

    if not os.path.exists('data'):
        os.makedirs('data')
    
    # # INITIALIZE SIMULATION:
    rows = 100
    cols = 100
    n_simulations = 100
    
    # datapoints = 20
    
    sim = WildFireSimulation(rows, cols)
    
    # d = np.linspace(0.1,1,datapoints)
    # c = np.zeros((datapoints,n_simulations))
    
    # for i,dd in enumerate(d):
    #     sim.set_params('grid_density', dd)
    #     counts = np.array([get_burnt(sim) for _ in range(n_simulations)])
    #     c[i] = counts
    #     print(i)
    # plt.scatter(d,c.mean(axis=1))

    # plotter = MakePlots(sim)
    # parameters = ['percentage_tree_1', 'wind_speed']
    # values = [[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    #          [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]]
    # for i, parameter in enumerate(parameters):
    #     # print(parameter, "-----", values[i])
    #     plotter.sensitivity_analysis(sim, parameter, values[i], n_simulations)

    visualizer = Visualize('Fire_data_n100.xlsx')
    visualizer.animate(sim, steps=200)
