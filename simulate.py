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
                    self.current_forest[row][col] = self.grid.burn_trees(neighbors)
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

if __name__=="__main__":
    # Example:
    rows = 50
    cols = 50
    steps = 100
    
    simulation = WildFireSimulation(rows, cols)
    simulation.animate(steps)
    