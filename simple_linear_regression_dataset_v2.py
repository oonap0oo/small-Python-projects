#!/usr/bin/env python3
#
#  simple_linear_regression_dataset_v2.py
#  
#  Copyright 2025 Nap0
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  This code explores 4 different methods for simple linear regression in Python
#  It uses a function directly coded in Python
#  From python's statistics library: function statistics.linear_regression()
#  From the Numpy library function numpy.polynomial.polynomial.Polynomial.fit()
#  From the Scipy library function nscipy.stats.linregress()
#  It plots the xy data and the linear regression lines
#  It displays a table using matplotlib underneath the plot 
#  the test data is the duration of one swing for different lengths of a pendulum
 
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec # align subplots also with variable size
import numpy as np


# xy data duration of one swing for different lengths of a pendulum
# length of the pendulum in cm
x_data = np.array([6.5, 11.0, 13.2, 15.0, 18.0, 23.1, 24.4, 26.6, 30.5, 34.3, 37.6, 41.5])
# duration of one swing in s
y_data = np.array([0.51, 0.68, 0.73, 0.79, 0.88, 0.99, 1.01, 1.08, 1.13, 1.26, 1.28, 1.32])

   
    
    
 # ****  PARAMETERS  ****
# plots
text_size = 18
color_plot_background = "#F0F0F0"
color_background = "#E0E0E0"
color_table_header = "#C0C0C0"
# ***********************


# print the data
print("Data: The length of a pendulum is changed and the duration of one swing is recorded for each length.\n")
print(f"{"length":>16}\t{"duration":>16}")
for x,y in zip(x_data, y_data):
    print(f"{x:>14} {"cm"}\t{y:>14} {"s"}")


# linear regression using a function directly coded in Python
# calculating the slope and intercept of a simple linear regression
# directly coded in Python
# approximation of y = slope.x + intercept
# slope = sum[ (xn - mean(x)).(yn - mean(y)) ] / sum[ (xn - mean(x))**2 ]
# intercept = mean(y) - slope.mean(x)
def simple_linear_regression(x, y):
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    slope = np.sum( (x - mean_x) * (y - mean_y) ) / np.sum( (x - mean_x)**2 )
    intercept = mean_y - slope * mean_x
    return(slope, intercept)
slope_python, intercept_python = simple_linear_regression(x_data, y_data)
print("\nMethod 1:")
print("Using a function directly coded in Python")
print(f"slope = {slope_python:.16f}, intercept = {intercept_python:.16f}")



# linear regression using python's statistics library 
from statistics import linear_regression
# function statistics.linear_regression()
slope_statistics, intercept_statistics = linear_regression(x_data, y_data)
print("\nMethod 2:")
print("Using statistics.linear_regression() from python's statistics library")
print(f"slope = {slope_statistics:.16f}, intercept = {intercept_statistics:.16f}")


# linear regression using numpy
from numpy.polynomial import Polynomial
# function numpy.polynomial.polynomial.Polynomial.fit()
numpy_regression= Polynomial.fit(x_data, y_data, 1)
intercept_numpy = numpy_regression.convert().coef[0]
slope_numpy = numpy_regression.convert().coef[1]
print("\nMethod 3:")
print("Using numpy.polynomial.polynomial.Polynomial.fit() from library numpy")
print(f"slope = {slope_numpy:.16f}, intercept = {intercept_numpy:.16f}")


# linear regression using scipy
from scipy.stats import linregress
# function nscipy.stats.linregress()
slope_scipy, intercept_scipy, r, p, se  = linregress(x_data, y_data)
print("\nMethod 4:")
print("Using nscipy.stats.linregress() from library scipy")
print(f"slope = {slope_scipy:.16f}, intercept = {intercept_scipy:.16f}")



# ******  PLOTTING  ******

# add a linear regression line to the plot using the slope and intercept values
# this function also uses the array x_values to calculate the y values of the line
# it adds a text label to the plot which is used in the legend
def plot_a_regression_line(slope, intercept, x_values, label_text):
    # calculating y values of the line
    regression_line_y = x_values * slope + intercept
    plt.plot(x_values, regression_line_y, label = label_text)


#starting a new plot

# gridspec object defines subplots and their relative size
gs = GridSpec(2, 1, width_ratios=[1], height_ratios=[3, 1])
    
    
fig = plt.figure(figsize = (15, 10), num = 1, facecolor = color_background)
plt.subplot(gs[0])
plt.title("Simple linear regression in Python using four different methods", 
            fontsize = text_size + 2, fontweight = "bold", y = 1.02)
plt.xlabel("Length of pendulum [cm]", fontsize = text_size)
plt.ylabel("Duration of one swing [s]", fontsize = text_size)
plt.tick_params(labelsize = text_size)
plt.gca().set_facecolor(color_plot_background) 
plt.grid(visible = True)


# plotting the xy data as scatter plot
plt.scatter(x_data, y_data, marker = "D", s=80, label = "xy data: Time of one swing for pendulums of varying length")


# linear regression using a function directly coded in Python
# see simple_linear_regression()
slope, intercept = simple_linear_regression(x_data, y_data)
# adding a linear regression line to the graph
label_text = "Using a function directly coded in Python"
plot_a_regression_line(slope_python, intercept_python, x_data, label_text)



# linear regression using python's statistics library 
# adding a linear regression line to the graph
label_text = "Using statistics.linear_regression()"
plot_a_regression_line(slope_statistics, intercept_statistics, x_data, label_text)


# linear regression using numpy
# adding a linear regression line to the graph
label_text = "Using numpy.polynomial.polynomial.Polynomial.fit()"
plot_a_regression_line(slope_numpy, intercept_numpy, x_data, label_text)


# linear regression using scipy
# adding a linear regression line to the graph
label_text = "Using scipy.stats.linregress()"
plot_a_regression_line(slope_scipy, intercept_scipy, x_data, label_text)

# add a legend to the plot
plt.legend(fontsize = text_size - 1)


# creating a second subplot to add a table
plt.subplot(gs[1])
plt.gca().set_facecolor(color_plot_background) 
plt.axis(False)
ndec = 15
table_col_labels = ["Method", "Slope", "Intercept"]
table_data = [
["Direct Python code", f"{slope_python:.{ndec}f}", f"{intercept_python:.{ndec}f}"],
["Statistics linear_regression()", f"{slope_statistics:.{ndec}f}", f"{intercept_statistics:.{ndec}f}"],
["Numpy Polynomial.fit()", f"{slope_numpy:.{ndec}f}", f"{intercept_numpy:.{ndec}f}"],
["Scipy stats.linregress()", f"{slope_scipy:.{ndec}f}", f"{intercept_scipy:.{ndec}f}"]
]
table_object = plt.table(table_data, colLabels = table_col_labels, 
        cellColours = [[color_plot_background] * 3] * 4, loc = "center",
        colColours = [color_table_header] * 3)
table_object.auto_set_font_size(False)
table_object.set_fontsize(text_size - 1)
table_object.scale(1, 3)



# define space between subplots
plt.subplots_adjust(hspace = 0.455, left = 0.08, right = 0.94, bottom = 0.11, top = 0.93)


# start with plot window maximized, this works at least in linux..
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

plt.show()
    
