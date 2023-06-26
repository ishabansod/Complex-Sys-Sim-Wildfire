from simulate import WildFireSimulation
from visualize import Visualize
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import statistics
import math

def get_burnt(sim,steps=-1): 
    sim.run(steps)
    burned = (sim.burned_trees)
    sim.reset()
    return burned

if __name__=="__main__":
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
    plt.hist(burned)
    plt.title("Distribution of final fire size for fixed density/vegetation/elevation/wind vector")
    plt.ylabel("Frequency")
    plt.xlabel("Final fire size $N_F$")
    plt.show()

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

