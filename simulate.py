from grid import Grid
import random
import numpy as np

class WildFireSimulation(Grid):
    def __init__(self, rows, cols):
        super().__init__(rows,cols)
        
        self.history = [] # stores a list of forest states
        self.history.append(np.copy(self.current_forest))
        self.converged = False

    def update_grid(self):
        # take current grid as input
        # if the cell is in state 1 (empty) or state 4 (burnt)
        # then the cell will remain in the same state
        # if the cell is in state 2 (tree) or state 3 (burning)
        # then the cell will be updated according to the rules

        state = self.history[-1]
        for row in range(1, self.rows - 1):
            for col in range(1, self.cols - 1):
                
                # burning cell becomes burnt
                if state[row][col] == 3:
                    if random.random() < 0.5:
                        self.current_forest[row][col] = 3
                    else:
                        self.current_forest[row][col] = 4
                        self.burned_trees += 1

                # get neighbors of tree patch, see if it burns or not
                if state[row][col] == 2:
                    neighbors = [
                        [state[i][j] for j in range(col - 1, col + 2)] for i in range(row - 1, row + 2)
                        ]
                    # neighbors = [
                    #     [state[i][j] for j in range(col - 1, col + 2) if (i, j) != (row, col)] for i in range(row - 1, row + 2)
                    #     ]
                    # print("-----------------",neighbors)
                    self.current_forest[row][col] = self.burn_trees(row, col, neighbors)
        if not np.array_equal(state, self.current_forest):
            self.history.append(np.copy(self.current_forest))
        else:
            self.converged = True
        return self.current_forest

    def run(self,steps=-1):
        
        step = 0
        
        while steps==-1 or step < steps:
            self.update_grid()
            if self.converged:
                break
            step += 1
    
    def reset(self):
        self.__init__(self.rows,self.cols)