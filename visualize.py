import copy
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import animation as animation
from matplotlib import colors
import numpy as np
import os

import openpyxl
import matplotlib.pyplot as plt
import numpy as np
import powerlaw

class Visualize():
    def __init__(self, workbook):
        self.cmap = colors.ListedColormap(['brown', 'green','red', 'black'])
        self.boundaries = [1, 1.5, 2.5, 3.5,4.5]
        self.norm = colors.BoundaryNorm(self.boundaries, self.cmap.N, clip=True)
        self.workbook = workbook


    
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
        # Iterate over each sheet
        for sheet_name in self.workbook.sheetnames:
            # Access the current sheet
            worksheet = self.workbook[sheet_name]

            # Iterate over each column in the sheet
            for column in worksheet.iter_cols():
                column_values = [cell.value for cell in column]

                # Remove None values from the column
                column_values = [value for value in column_values if value is not None]

                # Filter values lower than 10
                # column_values = [value for value in column_values if value >= 10]

                # Proceed only if there are values remaining
                if column_values:
                    # Create a histogram for the column
                    hist, bin_edges = np.histogram(column_values, bins='auto')

                    # Perform power-law analysis
                    fit = powerlaw.Fit(column_values, xmin=min(column_values), discrete=True)

                    # Calculate the KS statistic
                    ks_statistic = fit.power_law.KS()

                    # Print the estimated parameters and KS statistic
                    print("Sheet:", sheet_name)
                    print("Column:", column[0].column_letter)
                    print("Alpha (scale parameter):", fit.alpha)
                    print("Xmin (minimum value):", fit.xmin)
                    print("KS statistic:", ks_statistic)
                    print("")
                    # Plot the histogram and the power-law fit
                    plt.hist(column_values, bins=bin_edges, log=True, edgecolor='black', alpha=0.7)
                    fit.plot_pdf(color='red', linestyle='--', linewidth=2)
                    plt.xscale('log')
                    plt.yscale('log')
                    plt.xlabel('Value (log scale)')
                    plt.ylabel('Frequency (log scale)')
                    plt.title(f'Log-log Histogram with Power-Law Fit - {sheet_name} - {column[0].column_letter}\nAlpha = {fit.alpha:.4f}, Xmin = {fit.xmin:.4f}, KS = {ks_statistic:.4f}')
                    plt.legend(['Power-Law Fit', 'Histogram'])
                    plt.show()
        # Close the workbook after you're done
        self.workbook.close()
