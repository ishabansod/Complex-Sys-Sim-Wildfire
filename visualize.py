import copy
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import animation as animation
from matplotlib import colors
import numpy as np
import os
import pandas as pd

import openpyxl
import matplotlib.pyplot as plt
import numpy as np
import powerlaw

class Visualize():
    def __init__(self, filepath):
        self.cmap = colors.ListedColormap(['brown', 'green','red', 'black'])
        self.boundaries = [1, 1.5, 2.5, 3.5,4.5]
        self.norm = colors.BoundaryNorm(self.boundaries, self.cmap.N, clip=True)
        self.filepath = filepath


    
    def colormap(self, title, array):
        np_array = np.array(array)
        plt.figure()
        plt.imshow(np_array, interpolation="none", cmap=cm.viridis) # cmap=cm.Reds
        plt.colorbar()
        plt.title(title)
        plt.savefig(os.path.join('plots', title))
        plt.show()
    
    def show_grid(self,sim):
        self.colormap("Types of Trees Map", sim.trees)
        self.colormap("Density Map", sim.density)
        self.colormap("Altitude Map", sim.altitude)
        
    def animate(self,sim, steps):
        animations = []
        fig = plt.figure()
        for _ in range(steps):
            # update_grid()
            new_grid = copy.deepcopy(sim.update_grid())
            grid_arr = np.array(new_grid)

            # visualize
            ani = plt.imshow(grid_arr, animated=True, interpolation="none", cmap=self.cmap)
            animations.append([ani])
            
        gif = animation.ArtistAnimation(fig, animations, interval=100, blit=True,repeat_delay=100)
        gif.save('plots/gif-tree-type.gif')
        plt.show()

    
    def plot_distribution(self,sim):
        plot_empty = []
        plot_trees = []
        plot_burning = []
        plot_burned = []

        for state in sim.history:
            num_empty = np.count_nonzero(state == 1) #TODO empty may be removed
            num_trees = np.count_nonzero(state == 2) 
            num_burning = np.count_nonzero(state == 3)
            num_burned = np.count_nonzero(state == 4)

            plot_empty.append(num_empty)
            plot_trees.append(num_trees)
            plot_burning.append(num_burning)
            plot_burned.append(num_burned)

        time_steps = range(len(plot_empty))

        plt.figure()
        plt.plot(time_steps, plot_empty, label='Empty')
        plt.plot(time_steps, plot_trees, label='Trees')
        plt.plot(time_steps, plot_burning, label='Burning')
        plt.plot(time_steps, plot_burned, label='Burned')
        plt.xlabel('Time Step')
        plt.ylabel('Number of Cells')
        plt.title('Distribution of Cells over Time')
        plt.legend()
        plt.savefig('plots/plot_empty.png')


    def scaling_behavior(self):
        # Define the file path and sheet names
        file_path = self.filepath
        sheet_names = ['percentage_tree_1', 'prob_delta_dens1', 'wind_speed'] # Replace with the actual sheet names

        # Define a dictionary to store the best scores for each column
        best_scores = {}

        # Loop over each sheet
        for sheet_name in sheet_names:
            # Read the sheet into a pandas DataFrame
            df = pd.read_excel(file_path, sheet_name=sheet_name)

            # Get the maximum column index
            max_column_index = df.shape[1] - 1

            # Define the range of columns (A to K)
            column_range = list(range(max_column_index + 1))

            # Loop over each column in the range
            for column_index in column_range:
                # Extract the data from the column
                data = df.iloc[:, column_index].dropna().values

                # Fit the power-law distribution
                fit = powerlaw.Fit(data=data, discrete=True)

                print(f"Sheet: {sheet_name}, Column: {chr(ord('A') + column_index)}")
                print(fit.distribution_compare('power_law', 'lognormal'))
                print(fit.distribution_compare('power_law', 'exponential'))
                print(fit.distribution_compare('power_law', 'lognormal_positive'))
                print(fit.distribution_compare('power_law', 'stretched_exponential'))
                print(fit.distribution_compare('power_law', 'truncated_power_law'))
                print('-' * 30)