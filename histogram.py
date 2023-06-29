import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl
import powerlaw

def import_xlsx_file(file_path, column_number, parameter):
    df = pd.read_excel(file_path, sheet_name=parameter)
    desired_column = df.iloc[:, column_number - 1]
    return desired_column

def plot_loghist(data, bins):
    frequency, bins = np.histogram(data, bins=bins)
    #frequency, bins, _ = plt.hist(data, bins = bins, log=True)
    fire_size = (bins[:-1] + bins[1:]) / 2
    #plt.xscale('log')
    #plt.title("Distribution of final fire size for fixed density/vegetation/elevation/wind vector")
    #plt.ylabel("Frequency")
    #plt.xlabel("Final fire size $N_F$")
    #plt.show()
    return frequency, fire_size

def log_linear_regression(x, y, min_x):
    log_y=[0]*len(y)
    for i in range(0, len(y)):
        if y[i] != 0:
            log_y[i] = np.log10(y[i])
    log_x = np.log10(x)
    slope, intercept = np.polyfit(log_x[min_x:], log_y[min_x:], 1)
    x_fit = np.linspace(log_x[min_x], log_x[len(log_x)-1], len(log_x))
    y_fit = slope * x_fit + intercept

    # Calculate R_squared
    residuals = log_y - y_fit
    total_sum_squares = np.sum((log_y - np.mean(log_y))**2)
    residual_sum_squares = np.sum(residuals**2)
    r_squared = 1 - (residual_sum_squares / total_sum_squares)

    return log_x, log_y, x_fit, y_fit, slope, r_squared

def linearity_test(file_path, column_number, parameter):
    # Load in data
    burned = import_xlsx_file(file_path, column_number, parameter)

    # Generate histogram
    MIN, MAX = min(burned), max(burned)
    bins = 10 ** np.linspace(np.log10(MIN), np.log10(MAX), 40)
    frequency, fire_size = plot_loghist(burned, bins)

    # Apply linear regression
    log_fire_size, log_frequency, x_fit, y_fit, slope, r_squared = log_linear_regression(fire_size, frequency, np.argmax(frequency))

    # Plot linear fit
    plt.scatter(log_fire_size, log_frequency)
    plt.plot(x_fit, y_fit, color='red', label='Linear Fit')
    plt.title(f'Linear fit with R_squared: {r_squared:.2f} and Slope: {slope:.2f}')
    plt.ylabel('Log frequency')
    plt.xlabel("Log final fire size $N_F$")
    plt.show()
    return slope, r_squared, log_fire_size

file_path = 'data\\Fire_data_n500.xlsx'
parameter_list = ['percentage_tree_1', 'prob_delta_dens1']
R_squared_matrix = []
slope_matrix = []

slope, r_squared, log_fire_size = linearity_test(file_path, 8, parameter_list[0])

burned = import_xlsx_file(file_path, 0, parameter_list[0])
data = burned
fit = powerlaw.Fit(data=data, discrete=True)
print(fit.distribution_compare('power_law', 'lognormal'))
print(fit.distribution_compare('power_law', 'exponential'))
print(fit.distribution_compare('power_law', 'lognormal_positive'))
print(fit.distribution_compare('power_law', 'stretched_exponential'))
print(fit.distribution_compare('power_law', 'truncated_power_law'))