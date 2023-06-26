import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def import_xlsx_file(file_path):
    df = pd.read_excel(file_path)
    first_column = df.iloc[:, 0]
    return first_column

file_path = 'C:\\Users\\cyril\\OneDrive\\Documenten\\GitHub\\Complex-Sys-Sim-Wildfire\\burned.xlsx'
burned = import_xlsx_file(file_path)

def plot_loghist(data, bins):
    hist, bins = np.histogram(data, bins=bins)
    logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
    plt.hist(data, bins=logbins, log=True)
    plt.xscale('log')
    plt.title("Distribution of final fire size for fixed density/vegetation/elevation/wind vector")
    plt.ylabel("Frequency")
    plt.xlabel("Final fire size $N_F$")
    plt.show()

plot_loghist(burned, 100)