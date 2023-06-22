import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import random
import math

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.trees = self.init_trees(trees=True)
        self.density = self.init_density(density=True)
        self.altitude = self.init_altitude(altitude=True)
    
    def init_trees(self, trees=False):
        # three types - 1: agricultural areas, 2: shrubs and 3: pine trees
        tree_matrix = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        if not trees:  # only one type of tree
            for i in range(self.rows):
                for j in range(self.cols):
                    tree_matrix[i][j] = 1
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    if i < self.cols // 3:
                        tree_matrix[i][j] = 1 # agricultural areas
                    elif i <= (2 * self.cols) //3:
                        tree_matrix[i][j] = 2 # shrubs
                    else:
                        tree_matrix[i][j] = 3 # pine trees
        
        return tree_matrix 
    
    def init_density(self, density):
        # three types - 1: sparse, 2: normal and 3: dense
        density_matrix = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
    
        if not density:  # uniform tree density of the grid
            for i in range(self.rows):
                for j in range(self.cols):
                    density_matrix[i][j] = 1
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    if i < self.rows // 3:
                        density_matrix[i][j] = 1 # sparse
                    elif i <= (2 * self.rows) //3:
                        density_matrix[i][j] = 2 # normal
                    else:
                        density_matrix[i][j] = 3 # dense
        
        return density_matrix
    
    def init_altitude(self, altitude):
        alt_matrix = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        max_height = 10
        offset_x = 20
        offset_y = 20

        noise_factor = 0.3  # Adjust this to control the level of noise

        if not altitude:  # uniform grid height
            for i in range(self.rows):
                for j in range(self.cols):
                    alt_matrix[i][j] = 1
        else:  # mountain-like altitude distribution
            for i in range(self.rows):
                for j in range(self.cols):
                    # Calculate the distance of the cell from the offset center of the grid
                    distance = math.sqrt((i - self.rows/2 + offset_y)**2 + (j - self.cols/2 + offset_x)**2)

                    # Calculate the height of the mountain at that cell
                    height = max_height * math.exp(-0.1 * distance)

                    # Add random noise to the height
                    noise = random.uniform(-1, 1) * noise_factor
                    height += noise

                    # Assign the height to the cell in the grid
                    alt_matrix[i][j] = height
            
        return alt_matrix

    def is_diagonal(self, neighbor_row, neighbor_col, x, y):
        row_offset = abs(x - neighbor_row)
        col_offset = abs(y - neighbor_col)
        return row_offset != 0 and col_offset != 0


    def calc_slope(self, neighbor, cell, is_diagonal):
        #TODO decide constants
        #Calculate the slope based on paper
        length = 1 # length of square side (constant)
        if is_diagonal:
            Theta = math.atan((neighbor - cell) / length)
        else:
            Theta = math.atan((neighbor - cell) / (length * math.sqrt(2)))
        a = 1 #constant value
        return np.exp(a * Theta)
    
    def colormap(self, title, array):
        np_array = np.array(array)
        plt.figure()
        plt.imshow(np_array, interpolation="none", cmap=cm.viridis) # cmap=cm.Reds
        plt.colorbar()
        plt.title(title)
        plt.savefig(os.path.join('plots', title))
        plt.show()
    
    def visualize_trees(self):
        self.colormap("Types of Trees Map", self.trees)
    
    def visualize_density(self):
        self.colormap("Density Map", self.density)
    
    def visualize_altitude(self):
        self.colormap("Altitude Map", self.altitude)
    
    def init_grid(self):
        # states: 1- empty; 2- tree; 3- burning; 4- burnt
        # forest = [[2 for _ in range(self.cols)] for _ in range(self.rows)]
        grid_density = 0.3
        forest = [[1 if random.random() < grid_density else 2 for _ in range(self.cols)] for _ in range(self.rows)]
        start_fire_x = 0
        start_fire_y = self.rows // 2

        for row in range(start_fire_y - 1, start_fire_y + 2):
            for col in range(start_fire_x, start_fire_x + 2):
                forest[row][col] = 3  # start fire at the y axis center

        return forest
    
    def burn_trees(self, x, y, neighbors):
        # TODO add height, possibly wind too
        # probability of burning
        p = 0.5

        # probability of burning due to tree type       
        p_tree_type = {
            1: -0.3,
            2: 0,
            3: 0.4
        } # values from the ref paper
        p_tree = p_tree_type[self.trees[x][y]]

        # probability of burning due to density
        p_density_type = {
            1: -0.4,
            2: 0,
            3: 0.3
        } # values from the ref paper
        p_density = p_density_type[self.density[x][y]]

        #currently probability is calculated for each neighbor (TODO: can be changed)
        for row in range(3):
            for col in range(3):
                if neighbors[row][col] == 3:
                    diag = self.is_diagonal(row, col, x, y)
                    slope = self.calc_slope(self.altitude[row][col], self.altitude[x][y], diag)
                    burn_prob = p * (1 + p_tree) * (1 + p_density) * slope  # add other factors here 
                    if burn_prob > random.random():
                        return 3
        return 2

# example
# rows = 300
# cols = 300

# grid = Grid(rows, cols)
# grid.visualize_trees()
# grid.visualize_density()
# grid.visualize_altitude()

# forest = grid.init_forest()
