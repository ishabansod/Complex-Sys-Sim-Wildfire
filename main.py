from simulate import WildFireSimulation
from make_plots import MakePlots
from visualize import Visualize
import numpy as np
from tqdm import tqdm
import os
import matplotlib.pyplot as plt
import statistics
import math
import pandas as pd

if __name__=="__main__":

    if not os.path.exists('plots'):
        os.makedirs('plots')
    
    # Example:
    rows = 100
    cols = 100
    n_simulations=500
    
    sim = WildFireSimulation(rows, cols)
    
    # visualization = Visualize()
    
    # visualization.show_grid(sim)
    
    # visualization.animate(sim, steps=200) # with animation
    #visualization.plot_distribution(simulation)
    
    burned = [get_burnt(sim) for _ in range(n_simulations)]

    def plot_loghist(data, bins):
        hist, bins = np.histogram(data, bins=bins)
        logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
        plt.hist(data, bins=logbins, log=True)
        plt.xscale('log')
        plt.title("Distribution of final fire size for fixed density/vegetation/elevation/wind vector")
        plt.ylabel("Frequency")
        plt.xlabel("Final fire size $N_F$")
        plt.show()
    
    plot_loghist(burned, 100)

    def save_list_to_excel(data, file_path):
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)

    file_path = 'C:\\Users\\cyril\\OneDrive\\Documenten\\GitHub\\Complex-Sys-Sim-Wildfire\\burned.xlsx'
    save_list_to_excel(burned, file_path)

def calculate_confidence_interval(data):
        n = len(data)
        mean = statistics.mean(data)
        stdev = statistics.stdev(data)
        z = 1.96  # Z-value for a 95% confidence interval

        margin_of_error = z * (stdev / math.sqrt(n))
        confidence_interval = (mean - margin_of_error, mean + margin_of_error)

        return mean, confidence_interval

parameter_list = [0, 1]
burned_mean_list, burned_CI_list = [14], [[13.5, 14.5]]
mean, confidence_interval = calculate_confidence_interval(burned)
burned_mean_list.append(mean)
burned_CI_list.append(confidence_interval)

def plot_mean_with_confidence_intervals(parameter, mean, CI):
    lower_CI = [CI_element[0] for CI_element in CI]
    upper_CI = [CI_element[1] for CI_element in CI]
    plt.plot(parameter, mean, 'o-', label='Data')
    plt.fill_between(parameter, lower_CI, upper_CI, alpha=0.3, label='Confidence Intervals')
    plt.xlabel('Final fire size $N_F$')
    plt.ylabel('Frequency')
    plt.title("Distribution of final fire size for variating density/vegetation/elevation/wind vector")
    plt.legend()
    plt.show()

plot_mean_with_confidence_intervals(parameter_list, burned_mean_list, burned_CI_list)

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
