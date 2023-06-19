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

    def update_grid(self):
        # take current grid as input
        # if the cell is in state 1 (empty) or state 4 (burnt)
        # then the cell will remain in the same state
        # if the cell is in state 2 (tree) or state 3 (burning)
        # then the cell will be updated according to the rules

        new_forest = [[1 for _ in range(self.grid.cols)] for _ in range(self.grid.rows)]
        for row in range(1, self.grid.rows - 1):
            for col in range(1, self.grid.cols - 1):
                # empty or burnt
                if self.current_forest[row][col] == 1 or self.current_forest[row][col] == 4:
                    new_forest[row][col] = self.current_forest[row][col]

                # burning cell
                elif self.current_forest[row][col] == 3:
                    if random.random() < 0.5:
                        new_forest[row][col] = 3
                    else:
                        new_forest[row][col] = 4

                # get neighbors of tree patch, see if it burns or not
                elif self.current_forest[row][col] == 2:
                    neighbors = [
                        [self.current_forest[i][j] for j in range(col - 1, col + 2)] for i in range(row - 1, row + 2)
                    ]
                    # print("-----------------",neighbors)
                    new_forest[row][col] = self.grid.burn_trees(neighbors)
        self.current_forest = new_forest
        return self.current_forest
    
    def simulate(self, steps):
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
        # gif.save('gif.html')
        plt.show()


# Example:
rows = 50
cols = 50
steps = 100

simulation = WildFireSimulation(rows, cols)
simulation.simulate(steps)
