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
# Set min and max index values to fit on the x-axis
def log_linear_regression(x, y, min_x, max_x):
    log_y=[0]*len(y)
    for i in range(0, len(y)):
        if y[i] != 0:
            log_y[i] = np.log10(y[i])
    log_x = np.log10(x)
    slope, intercept = np.polyfit(log_x[min_x:max_x], log_y[min_x:max_x], 1)
    x_fit = np.linspace(log_x[min_x], log_x[max_x], len(log_x))
    y_fit = slope * x_fit + intercept

    # Calculate R_squared
    residuals = log_y - y_fit
    total_sum_squares = np.sum((log_y - np.mean(log_y))**2)
    residual_sum_squares = np.sum(residuals**2)
    r_squared = 1 - (residual_sum_squares / total_sum_squares)

    return log_x, log_y, x_fit, y_fit, slope, r_squared

log_fire_size, log_frequency, x_fit, y_fit, slope, r_squared = log_linear_regression(fire_size, frequency, 15, 35)

# Plot linear fit
plt.scatter(log_fire_size, log_frequency)
plt.text(1.6, 1.9, f'R_squared: {r_squared:.2f}', fontsize=12)
plt.text(1.6, 2, f'Slope: {slope:.2f}', fontsize=12)
plt.plot(x_fit, y_fit, color='red', label='Linear Fit')
plt.show()