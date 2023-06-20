from grid import Grid
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import animation as animation

class WildFireSimulation:
    def __init__(self, rows, cols):
        self.grid = Grid(rows, cols)
        self.current_forest = self.grid.init_grid()

        self.grid.visualize_trees() # to show how different trees are placed on the grid
        
        self.history = [] # stores a list of forest states
        self.history.append(np.copy(self.current_forest))

    def update_grid(self):
        # take current grid as input
        # if the cell is in state 1 (empty) or state 4 (burnt)
        # then the cell will remain in the same state
        # if the cell is in state 2 (tree) or state 3 (burning)
        # then the cell will be updated according to the rules

        state = self.history[-1]
        for row in range(1, self.grid.rows - 1):
            for col in range(1, self.grid.cols - 1):
                
                # burning cell becomes burnt
                if state[row][col] == 3:
                    if random.random() < 0.5:
                        self.current_forest[row][col] = 3
                    else:
                        self.current_forest[row][col] = 4

                # get neighbors of tree patch, see if it burns or not
                if state[row][col] == 2:
                    neighbors = [
                        [state[i][j] for j in range(col - 1, col + 2)] for i in range(row - 1, row + 2)
                        ]
                    # print("-----------------",neighbors)
                    self.current_forest[row][col] = self.grid.burn_trees(row, col, neighbors)
        self.history.append(np.copy(self.current_forest))
        return self.current_forest
    
    def animate(self, steps):
        animations = []
        fig = plt.figure()
        for _ in range(steps):
            # update_grid()
            new_grid = copy.deepcopy(self.update_grid())
            grid_arr = np.array(new_grid)

            # visualize
            ani = plt.imshow(grid_arr, animated=True, interpolation="none", cmap=cm.viridis)
            animations.append([ani])
            
        gif = animation.ArtistAnimation(fig, animations, interval=100, blit=True,repeat_delay=100)
        gif.save('gif.gif')
        plt.show()

    
    def plot_distribution(self, history):
        plot_empty = []
        plot_trees = []
        plot_burning = []
        plot_burned = []

        for state in history:
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
        plt.savefig('plot_empty.png')



if __name__=="__main__":
    # Example:
    rows = 100
    cols = 100
    steps = 150
    
    simulation = WildFireSimulation(rows, cols)
    simulation.animate(steps)
    simulation.plot_distribution(simulation.history)
    