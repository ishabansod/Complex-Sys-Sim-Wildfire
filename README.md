# Complex-Sys-Sim-Wildfire

## About
Simulating forest fires using 2D cellular automata to understand the dynamics, scaling laws, critical exponents and transitions.

This project is a (partial) implementation of the paper - [A cellular automata model for forest fire spread prediction](https://www.sciencedirect.com/science/article/pii/S0096300308004943)

![](https://github.com/ishabansod/Complex-Sys-Sim-Wildfire/blob/model/plots/gif-tree-type-dens-0.9.gif)

## Requirements
Please install the following packages before running the code
1. Python 3+ (tested with v3.11)
2. NumPy, SciPy, Matplotlib, Pandas, 
4. math, random, time, os, scipy
3. openpyxl, powerlaw

## How to run
Initialize simulation:
```
rows = 100
cols = 100
n_simulations = 100

sim = WildFireSimulation(rows, cols)
```
1. To see animation for one run
```
visualizer = Visualize('Fire_data_n100.xlsx')
visualizer.animate(sim, steps=200)
```

2. To see the effect of varying parameters
    - create a MakePlots object, run a loop over ranges of parameters and call sensitivity_analysis function
```
plotter = MakePlots(sim)
    parameters = ['percentage_tree_1', 'wind_speed', 'alpha']
    values = [[0, 10, 20],
             [2, 4, 6],
             [0.06, 0.07, 0.08]] # change corresponding param value ranges
    for i, parameter in enumerate(parameters):
        print(parameter, "-----", values[i])
        plotter.sensitivity_analysis(sim, parameter, values[i], n_simulations)
```

3. To see the power-law behaviour 
    - create a visualize object with the dataset you want to look at
    - then call the function scaling behavior

```
visualizer = Visualize('Fire_data_n100.xlsx') # change file-name here
visualizer.scaling_behavior()
```

4. To see the effect of clustering
    - run the clustering_analysis method of the MakePlotter class
    - parameters of the sweep are editable inside of make_plots.py
    - data analysis is done in clustering_plots.ipynb notebook

```
plotter = MakePlots(sim)
plotter.clustering_analysis()
```

### References
1. [A cellular automata model for forest fire spread prediction](https://www.sciencedirect.com/science/article/pii/S0096300308004943)
2. [Forest fire spread using cellular automata](https://www.sciencedirect.com/science/article/abs/pii/S0965997806001293 )
3. [Parallel CellularAutomaton Wildfire](https://github.com/XC-Li/Parallel_CellularAutomaton_Wildfire/tree/master)
4. [Introduction of self-organised critical forest fire model](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.69.1629)
5. [Design and implementation of an integrated GIS-based cellular automata model to characterise forest fire behaviour](https://www.sciencedirect.com/science/article/pii/S0304380007003626)
