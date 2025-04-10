#!/usr/bin/env python3
#
#  runge_kutta_python_code_exp_decay.py
#  
#  Copyright 2025 Kurt Moerman <nap0@nap0-lenovo>
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
#  Comparing three methods to solve a ODE
#  testing first-order Euler and fourth-order Runge-Kutta methods coded directly in Python
#  on a simple exponential decay system because it has an exact solution
#  comparing the results and execution time to the scipy function solve_ivp()

import numpy as np
import matplotlib.pyplot as plt
# import the scipy function solve_ivp(), which can solve systems of ODEs
from scipy.integrate import solve_ivp
# import time module to measure duration of the methods
import time


# function which returns the value of dy / dt 
# of the exponential decay system
# it is supplied with values t, y and system parameters
# t is not used here as the system is time invariant
def dy_dt(t, y, lambda_constant):
    return(-lambda_constant * y)
    

# the exponential decay system has the advantage that
# it's solution can be directly calulated as a test
# of the Euler and Runge-Kutta method
def expo_decay(time, lambda_constant, value_at_zero):
    value = value_at_zero * np.exp(-lambda_constant * time)
    return(value)
    
    
# function which calculates the next y value according to the
# fourth - order Runge-Kutta method
# it is supplied with previous value yn, time step h and the function
# which returns the dy_dt and describes the system    
def runge_kutta(t, yn, h, fun_dy_dt, parameter):
    k1 = fun_dy_dt(t, yn, parameter)
    k2 = fun_dy_dt(t, yn + h * k1 / 2.0, parameter)
    k3 = fun_dy_dt(t, yn + h * k2 / 2.0, parameter)
    k4 = fun_dy_dt(t, yn + h * k3, parameter)
    yn_plus_1 = yn + h * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
    return(yn_plus_1)
    

# function which calculates the next y value according to the
# first - order Euler method
# it is supplied with previous value yn, time step h and the function
# which returns the dy_dt and describes the system    
def euler_method(t, yn, h, fun_dy_dt, parameter):
    yn_plus_1 = yn + h * fun_dy_dt(t, yn, parameter)
    return(yn_plus_1)
    
    
# function that returns the relative error in per mille, works with arrays
def relative_error_permille(reference_value, other_value):
    return( np.abs( 1E3 * (reference_value - other_value) / reference_value) )
 
 
# function that returns the absolute error in parts per million, works with arrays
def absolute_error_ppm(reference_value, other_value):
    return( np.abs( reference_value - other_value) * 1E6 )
    
    
# function calculates the execution time of a code block in ms, returns a string expression
def time_difference_ms_str(Tstart, Tstop):
    time_diff_ms = (Tstop - Tstart) * 1e3
    return(f"{time_diff_ms:.3f}ms")


title = \
"""Using three different methods to solve a ODE.
Testing them on a simple exponential decay system, because it has an exact solution. 
"""
    
info = \
"""
Comparing three methods to solve a ODE on a simple exponential decay system
because it has an exact solution. 

Exponential decay       

dN(t)/dt = -λ.N(t)             
N(t) = Nₒ.exp(-λ.t)      

First-order Euler method coded directly in Python.

Euler method 

dy(x)/dx = F(y(x))
yₙ₊₁ = yₙ + h.F(yₙ) 

Fourth-order Runge-Kutta method coded directly in Python.

Runge–Kutta method 

dy(x)/dx = F(y(x))
yₙ₊₁ = yₙ + 1/6.h.(k1 + 2.k2 + 2.k3 + k4)
k1 = F(yₙ)              k2 = F(yₙ + 1/2.h.k1)
k3 = F(yₙ + 1/2.h.k2)   k4 = F(yₙ + h.k3)
"""

# parameters    
time_interval = 5.0
number_of_steps = 30000
time_step = time_interval / number_of_steps
time_delay_constant_lambda = 1.0
initial_value = 1.0
max_relative_error_scipy = 1e-5
max_absolute_error_scipy = 1e-9

# prepare ndarray with time values
time_values = np.linspace(0, time_interval, number_of_steps)

# calculate directly the solution using array calculation of numpy
exp_decay_directly_calculated = expo_decay(time_values, time_delay_constant_lambda, initial_value)

# apply the Runge-Kutta method coded in Python
y_values_runge_kutta = np.empty(number_of_steps)

Tstart = time.perf_counter() 
y_values_runge_kutta[0] = initial_value
for index in range(1, number_of_steps):
    y_values_runge_kutta[index] = runge_kutta(time_values[index], y_values_runge_kutta[index - 1], time_step, dy_dt, time_delay_constant_lambda)
Tstop = time.perf_counter()
time_runge_kutta_ms = time_difference_ms_str(Tstart, Tstop)

    
# apply the Euler method coded in Python
y_values_euler = np.empty(number_of_steps)

Tstart = time.perf_counter() 
y_values_euler[0] = initial_value
for index in range(1, number_of_steps):
    y_values_euler[index] = euler_method(time_values[index], y_values_euler[index - 1], time_step, dy_dt, time_delay_constant_lambda)
Tstop = time.perf_counter()
time_euler_ms = time_difference_ms_str(Tstart, Tstop)


# apply the scipy function solve_ivp(), according to the specification it's purpose is to:
# "Solve an initial value problem for a system of ODEs."

Tstart = time.perf_counter()
result = solve_ivp(dy_dt, (0.0, time_interval), [initial_value], \
    t_eval = time_values, args = (time_delay_constant_lambda,), rtol = max_relative_error_scipy, atol = max_absolute_error_scipy )
Tstop = time.perf_counter()
time_scipy_ms = time_difference_ms_str(Tstart, Tstop)


# unpack the calculated value from object result
y_values_scipy = result.y[0]

print(title)
print("The first and last 5 values:")
print(f"{'time':>10}\t{'Euler':>10}\t{'Runge-Kutta':>10}\t{'solve_ivp()':>10}\t{'Exact':>10}")
for time, euler, runge, scipy, exact in zip(time_values[:5], y_values_euler[:5], y_values_runge_kutta[:5], y_values_scipy[:5], exp_decay_directly_calculated[:5]):
    print(f"{time:>10.6f}s\t{euler:>10.8f}\t{runge:>10.8f}\t{scipy:>10.8f}\t{exact:>10.8f}")
print("...")    
for time, euler, runge, scipy, exact in zip(time_values[-5:], y_values_euler[-5:], y_values_runge_kutta[-5:], y_values_scipy[-5:], exp_decay_directly_calculated[-5:]):
    print(f"{time:>10.6f}s\t{euler:>10.8f}\t{runge:>10.8f}\t{scipy:>10.8f}\t{exact:>10.8f}")

results = \
f"""
Comparing results and execution time to scipy function solve_ivp().
Time constant is {time_delay_constant_lambda}s, initial value of {initial_value}
calculating {number_of_steps} points, over {time_interval}s.

* Runge-Kutta method coded in Python took {time_runge_kutta_ms}.
* Euler method coded in Python took {time_euler_ms}.
* Scipy function solve_ivp() took {time_scipy_ms}
   max. rel. error set to {max_relative_error_scipy:.0e} and
   max. abs. error set to {max_absolute_error_scipy:.0e}.
   solve_ivp(): local error estimates < atol + rtol * abs(y)
"""
print(results)



# **** plots ******************************************** 
        
char_size = 14
lt = 2

# create new figure object
fig = plt.figure(figsize = (15, 10), num = "Runge-Kutta 1")

# overal title
plt.suptitle(title, fontweight = "bold", size = char_size + 3)

# add subplot for image
ax = fig.add_subplot(221)
ax.set_xlim(0,1)
ax.set_ylim(0,1)
ax.text(0 , 0, results, fontsize = char_size + 1, fontname = "monospace")
ax.axis('off')

# add subplot for y values
ax = fig.add_subplot(222)
ax.plot(time_values, exp_decay_directly_calculated, linewidth = lt, color = "black", label = "Exponential decay exact solution")
ax.plot(time_values, y_values_runge_kutta, linewidth = lt, color = "blue", label = "the Runge-Kutta method coded in Python")
ax.plot(time_values, y_values_euler, linewidth = lt, color = "red", label = "the first-order Euler method coded in Python")
ax.plot(time_values, y_values_scipy, linewidth = lt, color = "green", label = "the scipy function solve_ivp()")
ax.legend(fontsize = char_size)
ax.set_xlabel("time", fontsize = char_size)
ax.set_ylabel("values", fontsize = char_size)
ax.set_title("Calculated values", fontsize = char_size + 2, y = 1.03)
ax.tick_params(labelsize = char_size)
ax.grid(visible = True)


# add subplot for abs error values
ax = fig.add_subplot(223)
deviation_runge_kutta_y_values = absolute_error_ppm(exp_decay_directly_calculated, y_values_runge_kutta)
ax.plot(time_values, deviation_runge_kutta_y_values, linewidth = lt, color = "blue", label = "absolute error Runge-Kutta method coded in Python")
deviation_euler_y_values = absolute_error_ppm(exp_decay_directly_calculated, y_values_euler)
ax.plot(time_values, deviation_euler_y_values, linewidth = lt, color = "red", label = "absolute error Euler method coded in Python")
deviation_scipy_y_values = absolute_error_ppm(exp_decay_directly_calculated, y_values_scipy)
ax.plot(time_values, deviation_scipy_y_values, linewidth = lt, color = "green", label = f"absolute error Scipy function solve_ivp(),\nmax. abs. error set to {max_absolute_error_scipy:.0e}")
ax.legend(fontsize = char_size)
ax.set_xlabel("time", fontsize = char_size)
ax.set_ylabel("Absolute erro (ppm)", fontsize = char_size)
ax.set_title("Absolute error in parts per million, using exact solution", fontsize = char_size + 2, y = 1.03)
ax.tick_params(labelsize = char_size)
ax.grid(visible = True)


# add subplot for ‰ rel error values
ax = fig.add_subplot(224)
deviation_percent_runge_kutta_y_values = relative_error_permille(exp_decay_directly_calculated, y_values_runge_kutta)
ax.plot(time_values, deviation_percent_runge_kutta_y_values, linewidth = lt, color = "blue", label = "relative error (%) Runge-Kutta method coded in Python")
deviation_percent_euler_y_values = relative_error_permille(exp_decay_directly_calculated, y_values_euler)
ax.plot(time_values, deviation_percent_euler_y_values, linewidth = lt, color = "red", label = "relative error (%) Euler method coded in Python")
deviation_percent_scipy_y_values = relative_error_permille(exp_decay_directly_calculated, y_values_scipy)
ax.plot(time_values, deviation_percent_scipy_y_values, linewidth = lt, color = "green", label = f"relative error (%) Scipy function solve_ivp(),\nmax. rel. error set to {max_relative_error_scipy:.0e}")
ax.legend(fontsize = char_size)
ax.set_xlabel("time", fontsize = char_size)
ax.set_ylabel("Relative error (‰)", fontsize = char_size)
ax.set_title("Relative error in per mille (‰), using exact solution", fontsize = char_size + 2, y = 1.03)
ax.tick_params(labelsize = char_size)
ax.grid(visible = True)

# define space between subplots
plt.subplots_adjust(wspace = 0.13, hspace = 0.3, left = 0.05, right = 0.98, bottom = 0.07, top = 0.87)

# start with plot window maximized, this works at least in linux..
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

plt.show()    




