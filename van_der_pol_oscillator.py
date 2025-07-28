# Van Der Pol Oscillator
# d(d(x)/dt)/dt -  μ * (1 - x**2) * dx/dt + x = A * sin( ω*t )
# μ: "mu" is non linear damping
# x: displacement
# A: amplitude of driving source
# ω: angular frequency of driving source [rad/s]
#
# d(d(x)/dt)/dt =  μ * (1 - x**2) * dx/dt - x + A * sin( ω*t )
#
##############################################
# converting to a system of 2 first order ODEs:
# dv/dt = μ * (1 - x**2) * v - x + A * sin( ω*t )
# dx/dt = v
##############################################
# v is velocity or derivative of displacement x over time


# import numpy library for its ndarray support
import numpy as np
# import the scipy function solve_ivp(), according to the specification it's purpose is to:
# "Solve an initial value problem for a system of ODEs."
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec # align subplots also with variable size
from PIL import Image # for loading a png image

# function defines output of driving source for the case where the olscillator is driven
def driving_source(time, omega, A):
    return A * np.sin(omega * time)

# defines system of undriven oscillator
# function has format required by the scipy solve_ivp() function
# it returns the derivatives of x and v over time
def vanderpol_undriven(time, x_and_v, mu):
    x, v = x_and_v
    dv_dt = mu * (1 - x**2) * v - x 
    dx_dt = v
    return([dx_dt, dv_dt])

# defines system of driven oscillator
# function has format required by the scipy solve_ivp() function
# it returns the derivatives of x and v over time
def vanderpol_driven(time, x_and_v, mu, omega, A):
    x, v = x_and_v
    dv_dt = mu * (1 - x**2) * v - x + driving_source(time, omega, A)
    dx_dt = v
    return([dx_dt, dv_dt])

#############################
# CASE 1: UNDRIVEN OSCILLATOR
#############################
# system parameters
# van der pol oscillator parameters
mu_undriven = 0.1
# initial values
x_and_v_init = [0, 0.1]
# parameters for calculation
number_of_steps = 20000 # total number of values calculated 
total_time = 125.0 # total time 
# prepare a tuple with the time interval, a mandatory argument for the scipy fucntion
time_interval = (0.0, total_time)
# prepare a numpy ndarray with the time points to be used
t = np.linspace(0, total_time, number_of_steps)

# calculations
print("Calculating undriven oscllator")
result = solve_ivp(vanderpol_undriven, time_interval, x_and_v_init, t_eval = t, args = ( mu_undriven, ))
print(result)
x_undriven, v_undriven = result.y
t_undriven = result.t

#############################
# CASE 2: DRIVEN OSCILLATOR
#############################
# system parameters
# van der pol oscillator parameters
mu_driven = 8.53
A = 1.2
omega = 2 * np.pi / 10
# initial values
x_and_v_init = [2, 0]
# parameters for calculation
number_of_steps = 20000 # total number of values calculated 
total_time = 125.0 # total time 
# prepare a tuple with the time interval, a mandatory argument for the scipy fucntion
time_interval = (0.0, total_time)
# prepare a numpy ndarray with the time points to be used
t = np.linspace(0, total_time, number_of_steps)

# calculations
print("Calculating driven oscllator")
result = solve_ivp(vanderpol_driven, time_interval, x_and_v_init, t_eval = t, args = ( mu_driven, omega, A ))
print(result)
x_driven, v_driven = result.y
t_driven = result.t
source_driving = driving_source(t, omega, A)

######################
# Plotting of results
######################

# parameters for the plots
text_size = 16
color_plot_background = "#F8F8F8"
color_background = "#E0E0E0"
colors_plot = ("#150086","#86001E","#008611")

# gridspec object defines subplots and their relative size
gs1 = GridSpec(2, 3, width_ratios=[1, 3, 1], height_ratios=[1,1])

# create new figure object
fig = plt.figure(figsize = (15, 10), num = "Van Der Pol Oscillator", facecolor = color_background)

# overal title
title = "Van Der Pol Oscillator"
plt.suptitle(title, fontweight = "bold", size = text_size + 4)

# subplot for image
ax = fig.add_subplot(gs1[0])
ax.set_facecolor(color_plot_background)
ax.set_xticks([])
ax.set_yticks([])
img = Image.open("van_der_pol_equation_undriven.png")
ax.imshow(img)

# plot f(t) undriven                 
plt.subplot(gs1[1])
plt.plot(t_undriven,x_undriven,
         label = "Undriven Oscillator, oscillator output x", color = "red", linewidth = 2)
plt.xlabel("time [s]", fontsize = text_size)
plt.ylabel("displacement", fontsize = text_size)
plt.tick_params(labelsize = text_size)
plt.gca().set_facecolor(color_plot_background) 
plt.grid(visible = True)
plt.title(f"Van De Pol Oscillator, undriven\n parameters: μ = {mu_undriven}, initial conditions: x0 = {x_and_v_init[0]}, v0 = {x_and_v_init[1]}", 
            fontsize = text_size + 1, fontweight = "bold", y = 1.02)

# phase plot undriven
plt.subplot(gs1[2])
plt.plot(x_undriven,v_undriven, label = "Undriven Oscillator, phase plot", color = "red")
plt.axis('square')
plt.xlabel("displacement x", fontsize = text_size)
plt.ylabel("velocity v", fontsize = text_size)
plt.tick_params(labelsize = text_size)
plt.gca().set_facecolor(color_plot_background) 
plt.grid(visible = True)
plt.title("Phase Plot", 
            fontsize = text_size + 1, fontweight = "bold", y = 1.02)

# subplot for image
ax = fig.add_subplot(gs1[3])
ax.set_facecolor(color_plot_background)
ax.set_xticks([])
ax.set_yticks([])
img = Image.open("van_der_pol_equation.png")
ax.imshow(img)

# plot f(t) driven                 
plt.subplot(gs1[4])
plt.plot(t_driven,x_driven,
         label = "oscillator output x", color = "blue", linewidth = 2)
plt.plot(t_driven,source_driving,
         label = "driving source", color = "green", linewidth = 2)
plt.xlabel("time [s]", fontsize = text_size)
plt.ylabel("displacement", fontsize = text_size)
plt.tick_params(labelsize = text_size)
plt.gca().set_facecolor(color_plot_background) 
plt.grid(visible = True)
plt.title(f"Van De Pol Oscillator, driven\n parameters: μ = {mu_driven}, A = {A}, ω = 2π/{2*np.pi/omega}, initial conditions: x0 = {x_and_v_init[0]}, v0 = {x_and_v_init[1]}", 
            fontsize = text_size + 1, fontweight = "bold", y = 1.02)
plt.legend(fontsize = text_size, loc = "lower right", ncols = 2)

# phase plot driven
plt.subplot(gs1[5])
plt.plot(x_driven,v_driven, label = "Driven Oscillator, phase plot", color = "blue")
#plt.axis('square')
plt.xlabel("displacement x", fontsize = text_size)
plt.ylabel("velocity v", fontsize = text_size)
plt.tick_params(labelsize = text_size)
plt.gca().set_facecolor(color_plot_background) 
plt.grid(visible = True)
plt.title("Phase Plot", 
            fontsize = text_size + 1, fontweight = "bold", y = 1.02)

# define space between subplots
plt.subplots_adjust(wspace = 0.186, hspace = 0.46, left = 0.005, right = 0.97, bottom = 0.07, top = 0.87)

# start with plot window maximized, this works at least in linux..
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

plt.show()
