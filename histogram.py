import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def import_xlsx_file(file_path):
    df = pd.read_excel(file_path)
    first_column = df.iloc[:, 0]
    return first_column

file_path = 'C:\\Users\\cyril\\OneDrive\\Documenten\\GitHub\\Complex-Sys-Sim-Wildfire\\Fire_data_n1000.xlsx'
burned = import_xlsx_file(file_path)

def plot_loghist(data, bins):
    hist, bins = np.histogram(data, bins=bins)
    logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
    n, bins, _ = plt.hist(data, bins=logbins, log=True)
    bin_centers = (logbins[:-1] + logbins[1:]) / 2
    plt.xscale('log')
    plt.title("Distribution of final fire size for fixed density/vegetation/elevation/wind vector")
    plt.ylabel("Frequency")
    plt.xlabel("Final fire size $N_F$")
    plt.show()

    print("Y-axis values:", n)
    print("Bin centers:", bin_centers)

#plot_loghist(burned, 100)


def plot_loghist2(data, bins):
    frequency, bins, _ = plt.hist(burned, bins = bins, log=True)
    fire_size = (bins[:-1] + bins[1:]) / 2
    plt.xscale('log')
    plt.title("Distribution of final fire size for fixed density/vegetation/elevation/wind vector")
    plt.ylabel("Frequency")
    plt.xlabel("Final fire size $N_F$")
    plt.show()
    return frequency, fire_size

# Settings histogram
MIN, MAX = min(burned), max(burned)
bins = 10 ** np.linspace(np.log10(MIN), np.log10(MAX), 40)
frequency, fire_size = plot_loghist2(burned, bins)

# Linear regression
log_frequency, log_fire_size = np.log10(frequency), np.log10(fire_size)
slope, intercept = np.polyfit(log_fire_size, log_frequency, 1)
x_fit = np.linspace(min(log_fire_size), max(log_fire_size), 100)
y_fit = slope * x_fit + intercept

# Plot linear fit
plt.scatter(log_fire_size, log_frequency)
#plt.plot(x_fit, y_fit, color='red', label='Linear Fit')
plt.show()