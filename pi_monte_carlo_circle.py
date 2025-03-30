#!/usr/bin/env python3
#
#  pi_monte_carlo_circle.py
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
#  Monte Carlo approximation of PI, using Python + Numpy
#  A series of points with random x,y coördinates are calculated, 
#  whether they fall inside the unit circle can be used to approximate the value of PI.
#  calculations are done in a series of parts called intervals
#  the code keeps track of the successive PI approximations taking the extra data into
#  account after each interval, it prints a table and plots a graph
#
import numpy as np
import matplotlib.pyplot as plt

# points are calculated in series of intervals
points_per_interval = 5000 
number_of_intervals = 25; 
total_number_of_points = points_per_interval * number_of_intervals

print("Monte Carlo approximation of PI, using Python + Numpy")
print("=====================================================\n")
print(f"Each interval has {points_per_interval} x and y values")
print(f"There are {number_of_intervals} intervals, total number of points is {total_number_of_points}")
print(f"{"interval":>12} |\t  {"N points":>12} |\t  {"N inside":>12} |\t {"PI approx.":>12} |")
print("------------------------------------------------------------------------------------")

# this variable will keep track of the number of points which fall insise unit circle
counted_points_inside_circle = 0 
# the approximations of PI after each interval, this is a numpy array
Pi_approximated = np.zeros(number_of_intervals)
# total the number of points after each interval, this is a numpy array
Number_of_points_calculated = np.zeros(number_of_intervals) 

# for-loop cycles through intervals only, the number crunching is done by numpy
for interval in range(number_of_intervals): 
    # random x and y values for the whole interval, these are numpy arrays
    X = np.random.rand(points_per_interval) 
    Y = np.random.rand(points_per_interval)
    # radius of all points in the interval, this is a numpy array
    Radius = np.sqrt( np.square(X) + np.square(Y) ) 
    # numpy array with boolean values showing whether the mpoints are inside the unit circle
    Inside_circle_or_not = np.less_equal(Radius, 1.0) 
    # number of True values in Inside_circle_or_not
    counted_points_inside_circle += np.count_nonzero(Inside_circle_or_not) 
    # total the number of points after each interval 
    Number_of_points_calculated[interval] =  points_per_interval * (interval + 1) 
    # approximation of pi using the data avau-ilable thus far
    Pi_approximated[interval] = 4.0 * counted_points_inside_circle / Number_of_points_calculated[interval] 
    # print line of table
    print(f"{interval + 1:>12} |\t  {Number_of_points_calculated[interval]:>12} |\t  {counted_points_inside_circle:>12} |\t {Pi_approximated[interval]:>12.7f} |")

# two matplotlib subplots
plt.figure(figsize=(15, 10), num = "Monte Carlo approximation of PI, using Python + Numpy")
# first subplot at the left of window
plt.subplot(1, 2, 1)
# as illustration the (x,y) points of the last interval
plt.scatter(X, Y , marker = ".", s = 4, label = "random x,y points")
# superimposed one quarter of the unit circle semi transparent
unit_circle = plt.Circle((0, 0), radius = 1, color="blue", alpha=.3, label = "Points inside unit circle")
plt.gca().add_artist(unit_circle)
# make this plot square and with axes going from 0 to 1
plt.axis('square')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xlabel("Random x values", fontsize = 15)
plt.ylabel("Random y values", fontsize = 15)
plt.title(f"Last interval of {points_per_interval} random points", fontsize = 18, y = 1.05)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.legend(fontsize = 15)
# second subplot at the right
plt.subplot(1, 2, 2)
# plot of the PI approximation reached after each interval versus the number of points calculated
plt.plot(Number_of_points_calculated, Pi_approximated, marker = "o", label = "Successive approxiation of PI")
# a horizontal line showing the numpy value of PI
plt.plot([0, total_number_of_points], [np.pi, np.pi], label = "Actual value of PI")
plt.axis([0, total_number_of_points, 3.1, 3.2])
plt.xlabel("Number of points calculated", fontsize = 15)
plt.ylabel("Approximation of PI", fontsize = 15)
plt.title(f"Successive approxiation of PI with {total_number_of_points} points", fontsize = 18, y=1.05)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()
plt.legend(fontsize = 15)
plt.tight_layout(pad=5.0)
plt.show()
