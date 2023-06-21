import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import random
from PIL import Image


class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.trees = self.init_trees(trees=True)
        self.density = self.init_density(density=True)
        self.altitude = self.init_altitude(altitude=True)

    def init_trees(self, trees=False):
        tree_matrix = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        if not trees:  # only one type of tree
            for i in range(self.rows):
                for j in range(self.cols):
                    tree_matrix[i][j] = 1
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    if j <= self.cols // 2:
                        tree_matrix[i][j] = 1
                    else:
                        tree_matrix[i][j] = 2

        return tree_matrix

    def init_density(self, density):
        den_matrix = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        if not density:  # tree density on the grid
            for i in range(self.rows):
                for j in range(self.cols):
                    den_matrix[i][j] = 1
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    if i < self.rows // 2:
                        den_matrix[i][j] = 1
                    else:
                        den_matrix[i][j] = 2

        return den_matrix

    def init_altitude(self, altitude):
        # TODO see how to incorporate this in burning probability
        alt_matrix = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        if not altitude:  # uniform grid height
            for i in range(self.rows):
                for j in range(self.cols):
                    alt_matrix[i][j] = 1
        else:  # mountain-like altitude distribution
            for i in range(self.rows):
                for j in range(self.cols):
                    alt_matrix[i][j] = abs(j - self.cols // 2) + abs(i - self.rows // 2)

        return alt_matrix

    def colormap(self, title, array):
        np_array = np.array(array)
        plt.imshow(np_array, interpolation="none", cmap=cm.viridis)
        plt.title(title)
        plt.show()

    def visualize_trees(self):
        self.colormap("Types of Trees Map", self.trees)

    def visualize_density(self):
        self.colormap("Density Map", self.density)

    def visualize_altitude(self):
        self.colormap("Altitude Map", self.altitude)

    def init_grid(self):
        # states: 1- empty; 2- tree; 3- burning; 4- burnt 5-house
        # forest = [[2 for _ in range(self.cols)] for _ in range(self.rows)]
        grid_density = 0.3
        forest = [[1 if random.random() < grid_density else 2 for _ in range(self.cols)] for _ in range(self.rows)]
        start_fire_x = self.cols // 2
        start_fire_y = self.rows // 2

        for row in range(start_fire_y - 1, start_fire_y + 2):
            for col in range(start_fire_x, start_fire_x + 2):
                forest[row][col] = 3  # make the center of the grid and neighbors burning

        # house coordinate
        forest[int(self.rows * 0.8)][int(self.cols * 0.8)] = 5

        return forest

    @staticmethod
    def load_map(image_path, rows, columns):
        # Load the image and resize it to the desired dimensions
        image = Image.open(image_path).resize((rows, columns))

        # Convert the image to RGB mode
        image_rgb = image.convert("RGB")

        # Define the blue color range
        blue_color = (157, 217, 243)  # RGB values for "#72cbff"
        tolerance = 30  # Adjust the tolerance value as needed

        # Create a grid of zeros with the same dimensions as the image
        grid = np.ones((rows, columns), dtype=int) * 2

        # Iterate over each pixel in the image
        for i in range(rows):
            for j in range(columns):
                # Get the RGB values of the pixel
                r, g, b = image_rgb.getpixel((i, j))

                # Check if the pixel color falls within the acceptable range
                if all(abs(channel - blue_channel) <= tolerance for channel, blue_channel in zip((r, g, b), blue_color)):
                    grid[i, j] = 1

        return grid

    def init_grid_map(self):
        forest = self.load_map("maps/amsterdam.PNG", self.rows, self.cols)
        start_fire_x = 0
        start_fire_y = self.rows // 2

        for row in range(start_fire_y - 1, start_fire_y + 2):
            for col in range(start_fire_x, start_fire_x + 2):
                forest[row][col] = 3  # make the center of the grid and neighbors burning

        # house coordinate
        forest[40][40] = 5

        return forest

    def burn_trees(self, neighbors):
        # TODO add tree types, density and height, possibly wind too
        # probability of burning
        p = 0.5

        if any(neighbors[row][col] == 3 for row in range(3) for col in range(3)):
            burn_prob = p  # add other factors here ?
            if burn_prob > random.random():
                return 3
        return 2

    def burn_house(self, neighbors):
        if any(neighbors[row][col] == 3 for row in range(3) for col in range(3)):
            return True

        return False


# Example usage:
# grid = Grid(50, 50)
# forest = grid.init_grid()

