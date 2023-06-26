import matplotlib.pyplot as plt
from simulate import WildFireSimulation
import os
import numpy as np
import scipy.stats as stats

class MakePlots:

    def __init__(self, simulation):
        self.simulation = simulation

    def sensitivity_analysis(self, sim, parameter, values, n_simulations):
        results = []
        for value in values:
            sim.set_params(parameter, value)
            burned = np.array([WildFireSimulation.get_burnt(sim) for _ in range(n_simulations)])
            mean = np.mean(burned)
            confidence_interval = stats.t.interval(0.95, len(burned)-1, loc=mean, scale=stats.sem(burned))
            results.append((value, mean, confidence_interval))

        # values for plotting
        values = [result[0] for result in results]
        means = np.array([result[1] for result in results])
        lower_ci = np.array([result[2][0] for result in results])
        upper_ci = np.array([result[2][1] for result in results])

        # Plot results
        plt.figure()
        plt.errorbar(values, means, yerr=[means - lower_ci, upper_ci - means], marker='o', linestyle='', label=parameter)
        plt.xlabel(parameter)
        plt.ylabel('Average Number of Burned Trees')
        plt.legend()

        # Saving in 'plots' folder
        filename = f'{parameter}_sensitivity.png'
        filepath = os.path.join('plots', filename)
        plt.savefig(filepath)
        plt.show()