import numpy as np
import random
import math

class Grid:
    def __init__(self, rows, cols):
        
        self.rows = rows
        self.cols = cols
        self.burned_trees = 0
        
        # auxiliary information grids
        self.trees = self.init_trees(percentage_trees= (50,50), trees=True, rand=False)
        self.density = self.init_density(density=True)
        self.altitude = self.init_altitude(altitude=True)
        self.wind = self.init_wind(wind=True)

        # main simulation grid
        self.current_forest = self.init_grid()
        
    ## MAIN GRID FOR SIMULATIONS ##
    
    def init_grid(self):
        # states: 1- empty; 2- tree; 3- burning; 4- burnt
        # forest = [[2 for _ in range(self.cols)] for _ in range(self.rows)]
        grid_density = 0.3
        edge = lambda row,col : row == 0 or col == 0 or row == self.rows-1 or col == self.cols-1
        forest = [[1 if random.random() < grid_density or edge(row,col) else 2 for col in range(self.cols)] for row in range(self.rows)]
        start_fire_x = random.randint(0, self.cols - 1)
        start_fire_y = random.randint(0, self.rows - 1)

        # forest[start_fire_x][start_fire_y] = 3  # start fire at a random point
        for row in range(start_fire_y - 1, start_fire_y + 2):
            for col in range(start_fire_x - 1, start_fire_x + 2):
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    forest[row][col] = 3  # start fire at a random point

        return forest
    
    def burn_trees(self, x, y, neighbors):
        # TODO add height, possibly wind too
        # probability of burning
        p = 0.5

        # probability of burning due to tree type       
        p_tree_type = {
            1: -0.5,
            2: 0.4
        } # values from the ref paper
        p_tree = p_tree_type[self.trees[x][y]]

        # probability of burning due to density
        p_density_type = {
            1: -0.4,
            2: 0,
            3: 0.3
        } # values from the ref paper
        p_density = p_density_type[self.density[x][y]]

        # probability of burning due to wind type
        p_wind = self.wind

        #currently probability is calculated for each neighbor (TODO: can be changed)
        for row in range(3):
            for col in range(3):
                if neighbors[row][col] == 3:
                    diag = self.is_diagonal(row, col, x, y)
                    slope = self.calc_slope(self.altitude[row][col], self.altitude[x][y], diag)
                    burn_prob = p * p_wind * (1 + p_tree) * (1 + p_density) * slope  # add other factors here 
                    if burn_prob > random.random():
                        return 3
        return 2
        
    ## AUXILIARY INFORMATION GRIDS ##
    
    def init_trees(self, percentage_trees=(30, 70), trees=True, rand = False):
        # two types - 1: agricultural areas and 2: pine trees
        tree_matrix = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        if not trees:  # only one type of tree
            for i in range(self.rows):
                for j in range(self.cols):
                    tree_matrix[i][j] = 1

        else:
            total_percentage = sum(percentage_trees)
            if total_percentage != 100:
                raise ValueError("The sum of percentages should be 100.")
            
            # randomly placed two types of trees
            if rand:
                shape = (self.rows, self.cols)
                length = self.rows * self.cols

                rest = [2]
                prob_type1 = percentage_trees[0]
                prob_base = (100 - prob_type1) // len(rest)

                num_type1 = round(length * (prob_type1 / 100))
                num_type2 = round(length * (prob_base / 100))

                # Make base 1D array
                base_arr = [1 for _ in range(num_type1)]
                for i in rest:
                    base_arr += [i for _ in range(num_type2)]
                base_arr = np.array(base_arr)

                # Give it a random order
                np.random.shuffle(base_arr)

                # Finally, reshape the array
                tree_matrix = base_arr.reshape(shape)
            
            # grid split straight accross
            else:
                curr_row = 0
                for i, percentage in enumerate(percentage_trees):
                    num_rows = (percentage * self.cols) // 100

                    for row in range(curr_row, curr_row + num_rows):
                        for j in range(self.rows):
                            if i == 0:
                                tree_matrix[j][row] = 1  # agricultural areas
                            elif i == 1:
                                tree_matrix[j][row] = 2  # pine trees
                    curr_row += num_rows

        return tree_matrix
    
    def init_wind(self, wind=False):
        # simplified burn probability depending on wind
        # Set initial conditions
        wind_speed = 10 #input('Give the speed of the wind in m/s:')
        wind_direction = 2* np.pi #input('Give the direction of the wind as angle between 0 and 2pi:')
        V = wind_speed
        theta = wind_direction # angle between fire propagation and wind direction
        c_1 = .045
        c_2 = .131
        f_t = np.exp(V * c_2 *(np.cos(theta)-1))
        p_w = np.exp(c_1 * V)*f_t
        return p_w

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

    ## HELPER FUNCTIONS ##

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
