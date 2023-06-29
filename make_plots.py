import matplotlib.pyplot as plt
import os
import numpy as np
import scipy.stats as stats
import time
from scipy.optimize import curve_fit
from tqdm import tqdm


class MakePlots:
    '''class to make plots with changing parameters'''
    def __init__(self, simulation):
        self.simulation = simulation

    def sensitivity_analysis(self, parameter, values, n_simulations):
        '''find burned trees for paramter values in given range'''
        results = []
        start_time = time.time()
        for i in range(0, len(values)):
            value = values[i]
            burned = []
            for _ in range(n_simulations):
                self.simulation.set_params(parameter, value)
                burned.append(self.simulation.get_burnt())
            
            # print("burned----", burned)
            mean = np.mean(burned)
            confidence_interval = stats.t.interval(0.95, len(burned)-1, loc=mean, scale=stats.sem(burned))
            results.append((value, mean, confidence_interval))

            # Saving burned list to excel file
            # workbook = openpyxl.load_workbook('Fire_data.xlsx')
            # sheet = workbook[parameter]
            # column_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
            # column_letter = column_letters[i]
            # # Iterate over the numbers and add them to the column
            # for j, number in enumerate(burned, start=1):
            #     cell = f'{column_letter}{j}'
            #     sheet[cell].value = number
            # workbook.save('Fire_data.xlsx')

        # Define values, mean and CI
        values = [result[0] for result in results]
        means = np.array([result[1] for result in results])
        lower_ci = np.array([result[2][0] for result in results])
        upper_ci = np.array([result[2][1] for result in results])

        # Plot results
        plt.figure()
        plt.fill_between(values, lower_ci, upper_ci, alpha=0.3, label='95% Confidence interval')
        plt.plot(values, means, 'o-', label=parameter)
        # plt.errorbar(values, means, yerr=[means - lower_ci, upper_ci - means], marker='o', linestyle='', label=parameter)
        plt.xlabel(parameter)
        plt.ylabel('Burned Trees')
        plt.grid()
        plt.legend()

        # Saving in 'plots' folder
        filename = f'{parameter}_sensitivity_00.png'
        filepath = os.path.join('plots', filename)
        plt.savefig(filepath)
        plt.show()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Computation time: {elapsed_time} seconds")
        
    def clustering_analysis(self):
        '''find burned trees for different degrees of clustering'''
        sim = self.simulation
        rows = sim.rows
        cols = sim.cols
        
        sim.make_deterministic() # turn off probabilities
        datapoints = 50 # how many densities to sweep
        density_param = np.linspace(0.35,0.6,datapoints)
        clustering = [0,0.5,1,1.5,2] # how much clustering to perform
        
        
        for i,c in enumerate(clustering): # for each degree of clustering
            
            points = []
            print('Clustering {} out of {}'.format(i,len(clustering)-1))
            
            for d in tqdm(density_param):
                
                sim.set_params('grid_density', d)
                                                
                sim.reset() # we reinitialize the forest to set the density
                
                sim.apply_voters_model(c) # we use the voters model to apply clustering 
                
                density = sim.total_trees/rows/cols
                if density < 0.35:
                    continue #we are not interested if the density gets too low due to clustering
                
                morans_i = sim.morans_i() # we quantify the clustering
                sim.run()
                percentage_burnt = sim.burned_trees/sim.total_trees
                
                points.append([density,morans_i,percentage_burnt])
                np.save('points{}'.format(i),points) # save points to analyze interactively (jupyter notebook)
                
        
        
    def sigmoid(self, x, x0, k):
        y = 1 / (1 + np.exp(-k*(x-x0)))
        return y
