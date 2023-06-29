from grid import Grid
import random
import numpy as np

class WildFireSimulation(Grid):
    '''class simulating the forest fire'''
    def __init__(self, rows, cols,init_params=True):
        super().__init__(rows,cols,init_params)
        
        self.history = [] # stores a list of forest states
        self.history.append(np.copy(self.current_forest))
        self.converged = False
        self.lit_tree = False

    def update_grid(self):
        '''use the current grid and use the transition rules, returns updated grid'''

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
        '''finds the state of a tree'''
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
                self.burned_trees += 1
            return tree_state
        
        return tree_state
    
    def get_correlation(self):
        
        state = self.history[-1].flatten()
        corrs = np.array([self.indicator(t1,t2,i,j) for i,t1 in enumerate(state) for j,t2 in enumerate(state[i+1:])])
        dist1, freq1 = np.unique(corrs[corrs[:,1]==1][:,0],return_counts=True)
        dist2, freq2 = np.unique(corrs[:,0],return_counts=True)
        rel_freq = []
        
        dist_iter = iter(dist2)
        item = next(dist_iter)
        j = 0
        for i,d in enumerate(dist1):
            while item != d:
                item = next(dist_iter)
                j += 1
            rel_freq.append(freq1[i]/freq2[j])
        m, b = np.polyfit(dist1,np.log(rel_freq),1)
        
        return -1/m
    
    def indicator(self,t1,t2,i,j):
        x1 = i // self.cols
        y1 = i % self.cols
        x2 = (i+j+1) // self.cols
        y2 = (i+j+1) % self.cols
        d = (x1-x2)**2+(y1-y2)**2
        if t1 == t2 and t1 == 4:
            return [d,1]
        return [d,0]
    
    def get_burnt(self,steps=-1): 
        '''counts the nuumber of burned trees in the grid'''
        self.run(steps)
        burned = self.burned_trees
        self.reset()
        return burned

    def run(self,steps=-1):
        '''updates the grid for number of steps'''
        step = 0
        while steps==-1 or step < steps:
            self.update_grid()
            if self.converged:
                break
            step += 1
    
    def reset(self):
        '''set the grid to default'''
        self.__init__(self.rows,self.cols,init_params=False)