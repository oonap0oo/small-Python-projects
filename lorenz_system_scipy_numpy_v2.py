#!/usr/bin/env python3
#
#  lorenz_system_scipy_numpy_v2.py
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
#  This code calculates a solution for the Lorenz System with the
#  system parameters sigma = 10, beta = 8.0 / 3.0, rho = 28.0
#  

# import numpy library for its ndarray support
import numpy as np

# import the scipy function solve_ivp(), according to the specification it's purpose is to:
# "Solve an initial value problem for a system of ODEs."
from scipy.integrate import solve_ivp

info = \
"""
Lorenz System of ODEs:

 dx                      dy                          dz
---- = σ(y - x)         ---- = x(ρ - z) - y         ---- = xy - βz
 dt                      dt                          dt
"""

# a function that defines the Lorenz system, 
# argumets and returned variable has to be as required by
# the scipy function solve_ivp()
def lorenz_system(time, xyz, sigma, beta , rho):
    x, y, z = xyz
    dx_dt = sigma * (y - x)
    dy_dt = x * (rho - z) - y
    dz_dt = x * y - beta * z
    return([dx_dt, dy_dt, dz_dt])

# **** parameters ***************

# parameters of the lorenz system
sigma = 10
beta = 8.0 / 3.0
rho = 28.0
      
# total number of values calculated 
number_of_steps = 10000

# total time in seconds covered
total_time = 100.0

# set initial conditions    
xyz_initial = [1.0, 1.0, 0.0]

# prepare a tuple with the time interval, an mandatory argument for the scipy fucntion
time_interval = (0.0, total_time)

# prepare a numpy ndarray with the time points to be used
time_points = np.linspace(0, 100, number_of_steps)

# call the scipy function which returns a specific object, here referenced by result
# additional arguments for function lorenz_system() have to be passed via a tuple as keyword parameter 'args'
result = solve_ivp(lorenz_system, time_interval, xyz_initial, t_eval = time_points, args = (sigma, beta , rho))

# unpack the calculated t,x,y,z values from the result object
x_values, y_values, z_values = result.y
t_values = result.t

# some output printed to console
title = f"Lorenz System using scipy.integrate.solve_ivp() in Python, {number_of_steps} points calculated"
print("\n" + title)
print("-" * len(title))
print(info)
print(f"{number_of_steps} values calculated, total time interval is {total_time} s")
print("Some of the first and last values of x, y and z:\n")
print(f"{"t  ":>10}\t{"x  ":>10}\t{"y  ":>10}\t{"z  ":>10}")
for t, x, y, z in zip(t_values[0:10], x_values[0:10], y_values[0:10], z_values[0:10]):
    print(f"{t:>10.4f} |\t{x:>10.6f} |\t{y:>10.6f} |\t{z:>10.6f}")
print(f"{"... ":>10}\t{"... ":>10}\t{"... ":>10}")
for t, x, y, z in zip(t_values[-10:], x_values[-10:], y_values[-10:], z_values[-10:]):
    print(f"{t:>10.4f} |\t{x:>10.6f} |\t{y:>10.6f} |\t{z:>10.6f}")


#plotting using matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec # align subplots also with variable size

# gridspec object defines subplots and their relative size
gs = GridSpec(3, 2, width_ratios=[1, 3], height_ratios=[1, 1, 1])

# create new figure object
fig = plt.figure(figsize = (15, 10), num = "Lorenz System 1")

# overal title
plt.suptitle(title, fontweight = "bold", size = 17)

# add subplot for x values
ax = fig.add_subplot(gs[0])
ax.plot(x_values, linewidth = 0.8, color = "blue")
ax.set_title("Values of x", fontweight = "bold", size = 15)

# add subplot for y values
ax = fig.add_subplot(gs[2])
ax.plot(y_values, linewidth = 0.8, color = "blue")
ax.set_title("Values of y", fontweight = "bold", size = 15)

# add subplot for z values
ax = fig.add_subplot(gs[4])
ax.plot(z_values, linewidth = 0.8, color = "blue")
ax.set_title("Values of z", fontweight = "bold", size = 15)

# add subplot for 3D line plot of x,y,z
ax = fig.add_subplot(gs[:,1],projection = "3d")
ax.plot(x_values, y_values, z_values, linewidth = 0.7, color = "red")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_title("3D plot of x vs y vs z", fontweight = "bold", size = 15)

# define space between subplots
plt.tight_layout(pad = 2)

# start with plot window maximized, this works at least in linux..
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

plt.show()    

