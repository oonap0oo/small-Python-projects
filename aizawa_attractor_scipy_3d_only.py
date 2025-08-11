#!/usr/bin/env python3

# import numpy library for its ndarray support
import numpy as np

# import the scipy function solve_ivp(), according to the specification it's purpose is to:
# "Solve an initial value problem for a system of ODEs."
from scipy.integrate import solve_ivp

info = \
"""
Aizawa Attractor:

dx/dt = (z - b) * x - d * y
dy/dt = d * x + (z - b) * y
dz_dt = c + a * z - z**3 / 3.0 - (x**2 + y**2) * (1 + e * z)  + f * z * x**3
"""

# a function that defines the Aizawa Attractor, 
# argumets and returned variable has to be as required by
# the scipy function solve_ivp()
def aizawa(time, xyz, a, b, c, d, e, f):
    x, y, z = xyz
    dx_dt = (z - b) * x - d * y
    dy_dt = d * x + (z - b) * y
    dz_dt = c + a * z - z**3 / 3.0 - (x**2 + y**2) * (1 + e * z)  + f * z * x**3
    return([dx_dt, dy_dt, dz_dt])

# **** parameters ***************

# parameters of the Aizawa attractor
a = 0.95
b = 0.7
c = 0.6
d = 3.5
e = 0.25
f = 0.1
      
# total number of values calculated 
number_of_steps = 25000

# total time in seconds covered
total_time = 150.0

# set initial conditions    
xyz_initial = [0.1, 0.0, 0.0]

# parameters for the plots
text_size = 14
color_plot_background = "black"
color_background = "black"
color_map = "hsv" # controls the coloring of the scatter plot points
color_grid = "#505050"
size_point = 5 # size of points of scatter plots; both 2d and 3d
fov_3d_deg = 110 # field of view in degrees which controlles the perspective rendering of 3D plot

# **** calculation ***************

# prepare a tuple with the time interval, an mandatory argument for the scipy fucntion
time_interval = (0.0, total_time)

# prepare a numpy ndarray with the time points to be used
time_points = np.linspace(0, total_time, number_of_steps)

print("Calling Scipy function solve_ivp()")
print(f"solve_ivp(aizawa, {time_interval}, {xyz_initial}, t_eval=time_points, \
args=({a}, {b}, {c}, {d}, {e}, {f}), method='LSODA')")

# call the scipy function which returns a specific object, here referenced by result
# additional arguments for function aizawa() have to be passed via a tuple as keyword parameter 'args'
result = solve_ivp(aizawa, time_interval, xyz_initial, t_eval=time_points,
                   args=(a, b, c, d, e, f), method='LSODA')

# abort here if the calculation was not succesfull
if not result.success:
    print(result.message)
    quit()

# unpack the calculated t,x,y,z values from the result object
x_values, y_values, z_values = result.y
t_values = result.t

# **** text output ***************

# some output printed to console
title = f"Aizawa Attractor using scipy.integrate.solve_ivp() in Python, {number_of_steps} points calculated"
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
print("\nLast values:",x_values[-1], y_values[-1], z_values[-1])


# **** plotting using matplotlib ***************

# import modules for plotting
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec # align subplots also with variable size

# use white elements on black background
plt.style.use('dark_background')

# create new figure object
fig = plt.figure(figsize = (15, 10), num = "Aizawa Attractor 2", facecolor = color_background)

# add subplot for 3D scatter plot of x,y,z
# calculate focal length out of field of view
focal_len = 1 / np.tan(np.radians(fov_3d_deg / 2))
print(f"focal length for 3D plot: {focal_len:.8} for a field of view of {fov_3d_deg}°")
ax = fig.add_subplot(111,projection = "3d")
ax.set_proj_type('persp', focal_length=focal_len)
ax.scatter(x_values, y_values, z_values, s = size_point, marker = ".", depthshade = False,
           c = z_values, cmap = color_map)
ax.set_facecolor(color_plot_background)
ax.set_axis_off()


# define space between subplots
plt.subplots_adjust(wspace = 0, hspace = 0, left = 0, right = 1, bottom = -0.4, top = 1.4)

# start with plot window maximized, this works at least in linux..
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

plt.show()    


