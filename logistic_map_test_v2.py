#!/usr/bin/env python3
#
#  logistic_map_test_v2.py
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
# Generating a bifurcation diagram of the Logistic Map
# using Numpy and Matplotlib
#
import matplotlib.pyplot as plt
import numpy as np

# total number of iterations, start and end value of parameter A
loops, astart, aend = int(2e6), 3.5, 4.0

# the numpy array to contain the x values of the logistic map is fllled with zeros
X = np.zeros(loops)
# the first value is initiated
X[0]=0.5

# the numpy array to contain the values for parameter a
A = np.linspace(astart, aend, loops)

# loops iterate the logistic map function for small increases of A
print(f"Iterating through {loops} steps, with values for A from {astart} to {aend}")
for index in range(loops - 1):
    X[index+1] = A[index] * X[index] * (1.0 - X[index])
print(f"Iterations complete, numpy arrays have lengths of A:{A.shape[0]} X:{X.shape[0]}")

# plot with dark background
plt.style.use('dark_background')
# set the size of the plot
plt.figure(figsize=(15, 10), num="Logistic map using Python, Numpy and Matplotlib")
# plot the many values of X versus A, the plot function does the imaging
plt.plot(A, X, ',', color='white', alpha=0.1)
# set title, labels and ticks
plt.gca().set_xlabel('a', fontsize=15)
plt.gca().set_ylabel('x', fontsize=15)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.axis('on')
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.07)
# make plot visible
plt.show()


