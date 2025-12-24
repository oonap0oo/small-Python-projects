# Rabinovich–Fabrikant System
# using info from https://en.wikipedia.org/wiki/Rabinovich%E2%80%93Fabrikant_equations

# import numpy library for its ndarray support
import numpy as np

# import the scipy function solve_ivp(), according to the specification it's purpose is to:
# "Solve an initial value problem for a system of ODEs."
from scipy.integrate import solve_ivp

info = \
"""
Rabinovich–Fabrikant System:

dx/dt = y * (z - 1 + x**2) + γ * x
dy/dt = x * (3 * z + 1 - x**2) + γ * y
dz/dt = -2 * z * (α + x * y)
"""

# a function that defines the Rabinovich–Fabrikant System, 
# arguments and returned variable has to be as required by
# the scipy function solve_ivp()
def rabinov(time, xyz, alpha, gamma):
    x, y, z = xyz
    dx_dt = y * (z - 1 + x**2) + gamma * x
    dy_dt = x * (3 * z + 1 - x**2) + gamma * y
    dz_dt = -2 * z * (alpha + x * y)
    return([dx_dt, dy_dt, dz_dt])

# **** parameters ***************

# parameters of the Rabinovich–Fabrikant System
# example 1
##alpha = 1.1
##gamma = 0.87
##x0 = -1.0
##y0 = 0.0
##z0 = 0.5
##total_time = 100.0 # total time in seconds covered
##number_of_steps = 20000 # total number of values calculated 

# example 2
##alpha = 0.05
##gamma = 0.1
##x0 = 0.1
##y0 = -0.1
##z0 = 0.1
##total_time = 100.0 # total time in seconds covered
##number_of_steps = 120000 # total number of values calculated 

# example 3
##alpha = 0.14
##gamma = 0.1
##x0 = 0.1
##y0 = -0.1
##z0 = 0.1
##total_time = 500.0 # total time in seconds covered
##number_of_steps = 60000 # total number of values calculated

# example 4
alpha = 0.14
gamma = 0.11
x0 = 0.1
y0 = -0.1
z0 = 0.1
total_time = 500.0 # total time in seconds covered
number_of_steps = 50000 # total number of values calculated 


# set initial conditions as list required by scipy function   
xyz_initial = [x0,y0,z0]

# parameters for the plots
text_size = 14
color_plot_background = "black"
color_background = "black"
color_map = "hsv" # controls the coloring of the scatter plot points
color_grid = "#707070"
size_point = 5 # size of points of scatter plots; both 2d and 3d
fov_3d_deg = 90 # field of view in degrees which controlles the perspective rendering of 3D plot

# **** calculation ***************

# prepare a tuple with the time interval, an mandatory argument for the scipy fucntion
time_interval = (0.0, total_time)

# prepare a numpy ndarray with the time points to be used
time_points = np.linspace(0, total_time, number_of_steps)

print("Calling Scipy function solve_ivp()")

# call the scipy function which returns a specific object, here referenced by result
# additional arguments for function rabinov() have to be passed via a tuple as keyword parameter 'args'
# example 4 requires the use of the "Radau" method
result = solve_ivp(rabinov, time_interval, xyz_initial, t_eval=time_points,
                   args=(alpha, gamma), method = "Radau")

# abort here if the calculation was not succesfull
if not result.success:
    print(result.message)
    quit()

# unpack the calculated t,x,y,z values from the result object
x_values, y_values, z_values = result.y
t_values = result.t

# **** text output ***************

# some output printed to console
title = f"Rabinovich–Fabrikant System using scipy.integrate.solve_ivp() in Python, {number_of_steps} points calculated"
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

title = f"""Rabinovich–Fabrikant System
alpha = {alpha}, gamma = {gamma}
x0 = {x0}, y0 = {y0}, z0 = {z0}
"""

# import modules for plotting
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec # align subplots also with variable size

# use white elements on black background
plt.style.use('dark_background')
plt.rcParams.update({'font.size': 16})
plt.rcParams['grid.color'] = color_grid
plt.rcParams['text.color'] = color_grid
plt.rcParams['axes.labelcolor'] = color_grid
plt.rcParams['xtick.color'] = color_grid
plt.rcParams['ytick.color'] = color_grid

# create new figure object
fig = plt.figure(figsize = (15, 10), num = "Rabinovich–Fabrikant System", facecolor = color_background)


# add subplot for 3D scatter plot of x,y,z
# calculate focal length out of field of view
focal_len = 1 / np.tan(np.radians(fov_3d_deg / 2))
print(f"focal length for 3D plot: {focal_len:.8} for a field of view of {fov_3d_deg}°")
ax = fig.add_subplot(111,projection = "3d")
ax.set_proj_type('persp', focal_length=focal_len)
ax.scatter(x_values, y_values, z_values, s = size_point, marker = ".", depthshade = False,
           c = np.sqrt(x_values**2 +  y_values**2 + z_values**2), cmap = color_map)
ax.set_facecolor(color_plot_background)
#ax.set_axis_off()
ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
ax.set_xlabel("x");ax.set_ylabel("y");ax.set_zlabel("z")
ax.set_title(title, color="white", y=0.8)

# define space between subplots
plt.subplots_adjust(wspace = 0, hspace = 0, left = 0, right = 1, bottom = -0.15, top = 1.15)

# start with plot window maximized, this works at least in linux..
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

plt.show()    


