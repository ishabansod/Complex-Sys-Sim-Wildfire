import matplotlib.pyplot as plt
from simulate import WildFireSimulation
import os
import numpy as np
import scipy.stats as stats
import openpyxl
import pandas as pd
import time

class MakePlots:

    def __init__(self, simulation):
        self.simulation = simulation

    def sensitivity_analysis(self, sim, parameter, values, n_simulations):
        results = []
        start_time = time.time()
        for i in range(0, len(values)):
            value = values[i]
            sim.set_params(parameter, value)
            burned = np.array([WildFireSimulation.get_burnt(sim) for _ in range(n_simulations)])
            mean = np.mean(burned)
            confidence_interval = stats.t.interval(0.95, len(burned)-1, loc=mean, scale=stats.sem(burned))
            results.append((value, mean, confidence_interval))

            # Saving burned list to excel file
            workbook = openpyxl.load_workbook('Fire_data.xlsx')
            sheet = workbook[parameter]
            column_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
            column_letter = column_letters[i]
            # Iterate over the numbers and add them to the column
            for j, number in enumerate(burned, start=1):
                cell = f'{column_letter}{j}'
                sheet[cell].value = number
            workbook.save('Fire_data.xlsx')

        # Define values, mean and CI
        values = [result[0] for result in results]
        means = np.array([result[1] for result in results])
        lower_ci = np.array([result[2][0] for result in results])
        upper_ci = np.array([result[2][1] for result in results])

        # Plot results
        #plt.figure()
        #plt.fill_between(values, lower_ci, upper_ci, alpha=0.3, label='95% Confidence interval')
        #plt.plot(values, means, 'o-', label=parameter)
        #plt.errorbar(values, means, yerr=[means - lower_ci, upper_ci - means], marker='o', linestyle='', label=parameter)
        #plt.xlabel(parameter)
        #plt.ylabel('Average Number of Burned Trees')
        #plt.legend()

        # Saving in 'plots' folder
        #filename = f'{parameter}_sensitivity.png'
        #filepath = os.path.join('plots', filename)
        #plt.savefig(filepath)
        #plt.show()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Computation time: {elapsed_time} seconds")