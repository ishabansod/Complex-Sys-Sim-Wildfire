# Wild Fire Simulation

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib import animation as animation


# initialize environment

def init_trees(n_row, n_col, trees=False):
    tree_matrix = [[0 for _ in range(n_col)] for _ in range(n_row)]
    
    if not trees:  # only one type of tree
        for i in range(n_row):
            for j in range(n_col):
                tree_matrix[i][j] = 1
    else:
        for i in range(n_row):
            for j in range(n_col):
                if j <= n_col // 2:
                    tree_matrix[i][j] = 1
                else:
                    tree_matrix[i][j] = 2
    
    return tree_matrix


def init_density(n_row, n_col, density):
    den_matrix = [[0 for _ in range(n_col)] for _ in range(n_row)]
    
    if not density:  # tree density on the grid
        for i in range(n_row):
            for j in range(n_col):
                den_matrix[i][j] = 1
    else:
        for i in range(n_row):
            for j in range(n_col):
                if j <= n_col // 2:
                    den_matrix[i][j] = 1
                else:
                    den_matrix[i][j] = 2 
    
    return den_matrix


def init_altitude(n_row, n_col, altitude):
    alt_matrix = [[0 for _ in range(n_col)] for _ in range(n_row)]
    
    if not altitude:  # uniform grid height
        for i in range(n_row):
            for j in range(n_col):
                alt_matrix[i][j] = 1
    else: # mountain-like altitude distribution
        for i in range(n_row):
            for j in range(n_col):
                alt_matrix[i][j] = abs(j - n_col // 2) + abs(i - n_row // 2)
    
    return alt_matrix

# draw initial condition in colour map
def colormap(title, array):
    np_array = np.array(array)
    plt.imshow(np_array, interpolation="none", cmap=cm.viridis)
    plt.title(title)
    plt.show()


# start simulation
n_row = 300
n_col = 300

trees = init_trees(n_row, n_col, trees=True)
density = init_density(n_row, n_col, density=True)
altitude = init_altitude(n_row, n_col, altitude=True)

colormap("Types of trres Map", trees)
colormap("Density Map", density)
colormap("Altitude Map", altitude)


# states: 1- empty; 2- tree; 3- burning; 4- burnt

# initialize forest and fire starting point
def init_forest(n_row, n_col):
    forest = [[2 for _ in range(n_col)] for _ in range(n_row)]

    start_fire_x = n_col // 2
    start_fire_y = n_row // 2

    for row in range(start_fire_x - 1, start_fire_x + 2):
        for col in range(start_fire_y - 1, start_fire_y + 2):
            forest[row][col] = 3 # make the centre of the grid and neighbors burning 

    return forest
