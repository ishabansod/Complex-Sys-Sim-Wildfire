from grid import Grid
import random
import numpy as np

class WildFireSimulation(Grid):
    def __init__(self, rows, cols):
        super().__init__(rows,cols)
        
        self.history = [] # stores a list of forest states
        self.history.append(np.copy(self.current_forest))
        self.converged = False
        self.lit_tree = False

    def update_grid(self):
        # take current grid as input
        # if the cell is in state 1 (empty) or state 4 (burnt)
        # then the cell will remain in the same state
        # if the cell is in state 2 (tree) or state 3 (burning)
        # then the cell will be updated according to the rules

        self.lit_tree = False        
        self.current_forest = [[self.tree_state(row,col) for col in range(self.cols)] for row in range(self.rows)]
        self.history.append(np.copy(self.current_forest))
        if self.lit_tree == False:
            self.converged = True
        
        return self.current_forest
    
    def tree_state(self,row,col):
        
        # edges do not change
        if row == 0 or col == 0 or row == self.rows-1 or col == self.cols-1:
            return 1
        
        state = self.history[-1]
        tree_state = state[row][col]
        
        if tree_state == 3:
            if random.random() < 0.5:
                self.lit_tree = True
                return 3
            else:
                self.burned_trees += 1
                return 4
        
        if tree_state == 2:
            neighbors = state[row-1:row+2,col-1:col+2]
            tree_state = self.burn_trees(row, col, neighbors)
            if tree_state == 3:
                self.lit_tree = True
            return tree_state
        
        return tree_state
    
    def get_burnt(sim,steps=-1): 
        sim.run(steps)
        burned = (sim.burned_trees)
        sim.reset()
        return burned

    def run(self,steps=-1):
        step = 0
        while steps==-1 or step < steps:
            self.update_grid()
            if self.converged:
                break
            step += 1
    
    def reset(self):
        self.__init__(self.rows,self.cols)