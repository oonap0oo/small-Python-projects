# This code calculates some solutions to an example Lotka–Volterra predator–prey model
# Function solve_ivp() is used from module Scipy to calculate solutions for 3 different initial conditions
#
#  Lotka–Volterra predator–prey model
#  ----------------------------------
#
#  dx                      dy                     
# ---- = α.x - β.x.y      ---- = -γ*y + δ.x.y     
#  dt                      dt               
#
# x is the population density of prey
# y is the population density of some predator
# α (alpha)is the maximum prey per capita growth rate
# β (beta)s the effect of the presence of predators on the prey death rate
# γ (gamma)is the predator's per capita death rate
# δ (delta)is the effect of the presence of prey on the predator's growth rate
#
# This code is shared in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# import numpy library for its ndarray support
import numpy as np
# import the scipy function solve_ivp(), according to the specification it's purpose is to:
# "Solve an initial value problem for a system of ODEs."
from scipy.integrate import solve_ivp

# a function that defines the predator–prey system, 
# argumets and returned variable has to be as required by
# the scipy function solve_ivp()
def lotka_volterra(time, xy, alpha, beta, gamma, delta):
    x, y = xy
    dx_dt = alpha * x - beta * x * y
    dy_dt = -gamma * y + delta * x * y
    return([dx_dt, dy_dt])

# **** parameters ***************
# parameters of the predator–prey system
alpha = 2
beta = 1
gamma = 2
delta = 0.95
xy_initial_values = ([4, 2], [6, 2],[8, 2])
# parameters for calculation
number_of_steps = 3000 # total number of values calculated 
total_time = 20.0 # total time 
# prepare a tuple with the time interval, a mandatory argument for the scipy fucntion
time_interval = (0.0, total_time)
# parameters for the plots
text_size = 16
color_plot_background = "#F8F8F8"
color_background = "#E0E0E0"
colors_plot = ("#150086","#86001E","#008611")

info = \
f"""Lotka–Volterra predator–prey model
 
 dx                      dy                     
---- = α.x - β.x.y      ---- = -γ*y + δ.x.y     
 dt                      dt               

x is the population density of prey
y is the population density of some predator
α (alpha) = {alpha}
β (beta) = {beta}
γ (gamma) = {gamma}
δ (delta) = {delta}"""

# prepare a numpy ndarray with the time points to be used
time_points = np.linspace(0, total_time, number_of_steps)

# call the scipy function for each initial condition
# the function returns a specific object, here stored in the list results
# additional arguments for function lotka_volterra() have to be passed via a tuple as keyword parameter 'args'
results = []
for xy_initial in xy_initial_values:
    results.append( solve_ivp(lotka_volterra, time_interval, xy_initial, 
                t_eval = time_points, args = (alpha, beta, gamma, delta)) )

# ***********  plotting using matplotlib  ***********
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec # align subplots also with variable size

# gridspec object defines subplots and their relative size
gs1 = GridSpec(3, 2, width_ratios=[3, 2], height_ratios=[1,1,1])
gs2 = GridSpec(2, 2, width_ratios=[3, 2], height_ratios=[1,2])

# create new figure object
fig = plt.figure(figsize = (15, 10), num = "Lotka–Volterra predator–prey model", facecolor = color_background)

# overal title
title = "Lotka–Volterra predator–prey model using Scipy function solve_ivp() in Python"
plt.suptitle(title, fontweight = "bold", size = text_size + 4)

# add subplot for values vs time
for index, result in enumerate(results):
    ax = fig.add_subplot(gs1[2 * index])
    ax.set_title(f"Values versus time for initial conditions: xo = {xy_initial_values[index][0]}, yo = {xy_initial_values[index][1]}", fontweight = "bold", size = text_size, y = 1.01)
    #ax.set_xlabel("time", fontsize = text_size)
    ax.set_ylabel("x,y values", fontsize = text_size)
    ax.set_facecolor(color_plot_background)
    # unpack the calculated t,x,y values from the result object
    x_values, y_values = result.y
    t_values = result.t
    ax.plot(t_values, x_values, linewidth = 2, 
        linestyle = "--",
        label = f"x values", 
        color = colors_plot[index])
    ax.plot(t_values, y_values, linewidth = 2, 
        linestyle = "-",
        label = f"y values", 
        color = colors_plot[index])
    ax.legend(fontsize = text_size)
    ax.tick_params(labelsize = text_size)
    ax.grid(visible = True)

# add subplot for info text
ax = fig.add_subplot(gs2[1])
ax.set_xlim(0,1)
ax.set_ylim(0,1)
tx = ax.text(0 , 1, info, fontsize = text_size - 1, 
        fontname = "monospace", 
        verticalalignment = "top")
tx.set_bbox(dict(facecolor = color_plot_background))
ax.axis('off')

# add subplot for Phase-space plot
ax = fig.add_subplot(gs2[3])
ax.set_title("Phase-space plot", fontweight = "bold", size = text_size, y = 1.01)
ax.set_xlabel("x value", fontsize = text_size)
ax.set_ylabel("y value", fontsize = text_size)
ax.set_facecolor(color_plot_background)
for index, result in enumerate(results):
    # unpack the calculated t,x,y values from the result object
    x_values, y_values = result.y
    t_values = result.t
    ax.plot(x_values, y_values, linewidth = 2, 
        label = f"xy values, xo = {xy_initial_values[index][0]}, yo = {xy_initial_values[index][1]}",
        color = colors_plot[index])
ax.legend(fontsize = text_size)
ax.tick_params(labelsize = text_size)
ax.grid(visible = True)

# define space between subplots
plt.subplots_adjust(wspace = 0.13, hspace = 0.4, left = 0.05, right = 0.98, bottom = 0.07, top = 0.88)

# start with plot window maximized, this works at least in linux..
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

plt.show()    


    
