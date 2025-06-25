# Driven damped pendulum
# I*d(dθ/dt)/dt + m*g*l*sin(θ) + b*dθ/dt = a*cos(Ω*t)
# I = m*l**2 : moment of inertia
# each term is torque
# d(dθ/dt)/dt = 1/I*( -g*m*l*sin(θ) - b*dθ/dt + a*cos(Ω*t) )
# dθ/dt = ω
# d(dθ/dt)/dt = dω/dt
######################################################
# system of 1 order ODE:
# dω/dt = 1/I*( -g*m/l*sin(θ) - b*ω + a*cos(Ω*t) )
# dθ/dt = ω
######################################################
# m: mass at end of pendulum
# l: length pendulum
# θ: angular deflection of pendulum
# ω: angular speed of pendulum
# I: moment of inertia
# g: gravitational acceleration
# b: friction coefficient propotional to angular speed
# a: amplitude of driving torque
# Ω: angular frequency of driving force

# import numpy library for its ndarray support
import numpy as np
# import the scipy function solve_ivp(), according to the specification it's purpose is to:
# "Solve an initial value problem for a system of ODEs."
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec # align subplots also with variable size
from PIL import Image # for loading a png image

def driving_torque(time, omega_driven, a):
    return -a*np.cos(omega_driven*time)

def pendulum(time, theta_omega, g, l, b, I, omega_driven,a):
    theta, omega=theta_omega
    t1=-g*I/l*np.sin(theta) # deflection pendulum
    t2=-b*omega # damping
    t3=a*np.cos(omega_driven*time) # driving torque
    domega_dt = (t1+t2+t3)/I
    dtheta_dt = omega
    return([dtheta_dt, domega_dt])


# system parameters
# constant 
g=9.81
# parameters
l=1 #length pendulum in meter
b=0.4 #degree of damping
m=1 #mass mendulum weight in kg
omega_driven=2*np.pi*1 #angular frequency driving force
a=8 #amplitude driving force
# parameters for the plots
text_size = 16
color_plot_background = "#F8F8F8"
color_background = "#E0E0E0"
colors_plot = ("#150086","#86001E","#008611")
# initial values
theta_omega_init = [np.radians(45), 0]
#moment of inertia
I=m*l**2 # calculating I once here iso. in each iteration
# parameters for calculation
number_of_steps = 3000 # total number of values calculated 
total_time = 25.0 # total time 
# prepare a tuple with the time interval, a mandatory argument for the scipy fucntion
time_interval = (0.0, total_time)
# prepare a numpy ndarray with the time points to be used
t = np.linspace(0, total_time, number_of_steps)

result = solve_ivp(pendulum, time_interval, theta_omega_init, t_eval = t, args = (g, l, b, I, omega_driven, a))
theta, omega = result.y
driving = driving_torque(t,omega_driven,a)

# gridspec object defines subplots and their relative size
gs1 = GridSpec(1, 2, width_ratios=[1, 4], height_ratios=[1])
gs2 = GridSpec(2, 2, width_ratios=[1, 4], height_ratios=[2, 1])

# create new figure object
fig = plt.figure(figsize = (15, 10), num = "Driven, damped pendulum", facecolor = color_background)

# overal title
title = "Driven, damped pendulum"
plt.suptitle(title, fontweight = "bold", size = text_size + 4)

# subplot for image
ax = fig.add_subplot(gs1[0])
ax.set_facecolor(color_plot_background)
ax.set_xticks([])
ax.set_yticks([])
img = Image.open("pendulum.png")
ax.imshow(img)

plt.subplot(gs2[1])
plt.plot(t,np.degrees(theta))
plt.xlabel("time [s]", fontsize = text_size)
plt.ylabel("angle of pendulum [degrees]", fontsize = text_size)
plt.tick_params(labelsize = text_size)
plt.gca().set_facecolor(color_plot_background) 
plt.grid(visible = True)
plt.title("Pendulum", 
            fontsize = text_size + 2, fontweight = "bold", y = 1.02)

plt.subplot(gs2[3])
plt.plot(t,driving)
plt.xlabel("time [s]", fontsize = text_size)
plt.ylabel("driving torque [Nm]", fontsize = text_size)
plt.tick_params(labelsize = text_size)
plt.gca().set_facecolor(color_plot_background) 
plt.grid(visible = True)
plt.title("Driving torque", 
            fontsize = text_size + 2, fontweight = "bold", y = 1.02)

# define space between subplots
plt.subplots_adjust(wspace = 0.15, hspace = 0.38, left = 0.02, right = 0.97, bottom = 0.07, top = 0.87)

# start with plot window maximized, this works at least in linux..
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())


plt.show()
