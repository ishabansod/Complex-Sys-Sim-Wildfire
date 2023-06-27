from simulate import WildFireSimulation
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
    
    # INITIALIZE SIMULATION:
    rows = 100
    cols = 100
    n_simulations=2
    
    datapoints = 20
    
    sim = WildFireSimulation(rows, cols)
    
    d = np.linspace(0.1,1,datapoints)
    c = np.zeros((datapoints,n_simulations))
    
    for i,dd in enumerate(d):
        sim.set_params('grid_density', dd)
        counts = np.array([get_burnt(sim) for _ in range(n_simulations)])
        c[i] = counts
        print(i)
    plt.scatter(d,c.mean(axis=1))
