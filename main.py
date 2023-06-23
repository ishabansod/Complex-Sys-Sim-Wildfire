from simulate import WildFireSimulation
from visualize import Visualize
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

def get_burnt(sim,steps=-1): 
    sim.run(steps)
    burned = (sim.burned_trees)
    sim.reset()
    return burned

if __name__=="__main__":
    # Example:
    rows = 100
    cols = 100
    n_simulations=100
    
    sim = WildFireSimulation(rows, cols)
    
    # visualization = Visualize()
    
    # visualization.show_grid(sim)
    
    # visualization.animate(sim, steps=200) # with animation
    #visualization.plot_distribution(simulation)
    
    burned = [get_burnt(sim) for _ in range(n_simulations)]
    plt.hist(burned)
    plt.show()