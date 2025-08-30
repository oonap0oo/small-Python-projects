# numerically solve ssytem of twe 1e order differential equations
# dy/dx = f(x,y,z)
# dz/dx = g(x,y,z)
# using scipy
# plot solution and draw phase plot

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec # align subplots also with variable size
from scipy.integrate import solve_ivp

# some examples of ODEs with parameters
# example 1: 2 order homogeneous linear ODE
# -----------------------------
# d²z/dx² + 1/5 * dz/dx + z = 0
# d²z/dx² = -z - 1/5 * dz/dx
# dy/dx = d²z/dx²
# dy/dx = -z-y/5, dz/dx = y
# number, dy/dx = f(x,y,z), dz/dx = f(x,y,z), x_start, x_stop, y_start, z_start
#
# example 2: Lotka–Volterra predator–prey model
# ----------------------------------------------
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
# example 3: Van Der Pol Oscillator
# ---------------------------------
# d²x/dt² -  μ * (1 - x**2) * dx/dt + x = A * sin( ω*t )
# μ: "mu" is non linear damping
# x: displacement
# A: amplitude of driving source
# ω: angular frequency of driving source [rad/s]
#
# d²x/dt² =  μ * (1 - x**2) * dx/dt - x + A * sin( ω*t )
#
# converting to a system of 2 first order ODEs:
# dv/dt = μ * (1 - x**2) * v - x + A * sin( ω*t )
# dx/dt = v
# v is velocity or derivative of displacement x over time
#
# example 4: Driven damped pendulum
# ---------------------------------
# I*d²θ/dt² + m*g*l*sin(θ) + b*dθ/dt = a*cos(Ω*t)
# I = m*l**2 : moment of inertia
# each term is torque
# d(dθ/dt)/dt = 1/I*( -g*m*l*sin(θ) - b*dθ/dt + a*cos(Ω*t) )
# dθ/dt = ω
# d(dθ/dt)/dt = dω/dt
#
# system of 1 order ODE:
# dω/dt = 1/I*( -g*m/l*sin(θ) - b*ω + a*cos(Ω*t) )
# dθ/dt = ω
#
# m: mass at end of pendulum
# l: length pendulum
# θ: angular deflection of pendulum
# ω: angular speed of pendulum
# I: moment of inertia
# g: gravitational acceleration
# b: friction coefficient propotional to angular speed
# a: amplitude of driving torque
# Ω: angular frequency of driving force
#
# example 5: Duffing equation
# ---------------------------
# d²y/dt² + δ*dy/dt + α*y +  β*y³ = γ*cos(ω*x)
# dy/dt = z
# dz/dt = -δ*z - α*y -  β*y³ + γ*cos(ω*x)
# δ, α, β, γ, ω are constants
# δ: amount of damping
# α: controls the linear stiffness
# β: amount of non-linearity in the restoring force;
#    if β = 0 the Duffing equation describes a damped and driven simple harmonic oscillator
# γ: is the amplitude of the periodic driving force;
#    if γ = 0  the system is without a driving force
# ω:  is the angular frequency of the periodic driving force
#  ( α = 1 , β = 5 , δ = 0.02 , γ = 8 , and ω = 0.5 )
#
# example 6: Brusselator
# ----------------------
# dy/dx = A + z*y**2 - B*y - y
# dz/dx = B*y - z*y**2
# fixed point: y=A, z=B/A
# fixed point becomes unstable when B > 1+A**2
# (A=1, B=3)
#
# example 7: Non linear second order ODE
# ---------------------------
# d²y/dx² + x*y = sin(x)
# dy/dx = z => d²y/dx² = dz/dx
# dz/dx = sin(x) - x*y
#
# Tuples containing the examples data
examples = (
            (1, "Second order homogeneous linear ODE, d²z/dx² + 1/5 * dz/dx + z = 0", "-z-y/5","y", 0.0, 30.0, 1.0, 0.0),
            (2, "Lotka–Volterra predator–prey model", "2*y-y*z","-2*z+0.95*y*z", 0.0, 12.0, 8.0, 2.0),
            (3, "Van Der Pol Oscillator, d²x/dt² -  μ * (1 - x**2) * dx/dt + x = A * sin( ω*t )", "0.1*(1-z**2)*y-z","y", 0.0, 120.0, 0.0, 0.1),
            (4, "Driven damped pendulum, I*d²θ/dt² + m*g*l*sin(θ) + b*dθ/dt = a*cos(Ω*t)", "9.8*sin(z)-0.3*y+cos(5*x)","y", 0.0, 36.0, 0.0, 0.0),
            (5, "Duffing equation, d²y/dt² + δ*dy/dt + α*y +  β*y³ = γ*cos(ω*x)","z", "-0.02*z-y-5*y**3+8*cos(0.5*x)",0.0, 80.0, 1.0, 1.0), 
            (6, "Brusselator","1+z*y**2-3*y-y", "3*y-z*y**2",0.0, 30.0, 1.0, 1.0),
            (7, "Non linear second order ODE, d²y/dx² + x*y = sin(x)","z", "sin(x)-x*y",0.0, 20.0, 1.0, 0.0),
            )

# dict holding functions which van be used in eval()
# using numpy functions to be able to process arrays
# so scipy function solve_ivp() can use eval() directly
math_fun_dict = {   
  "pi": np.pi, "e": np.e, "sqrt": np.sqrt,
  "log": np.log, "exp": np.exp, "log10": np.log10,
  "sin": np.sin, "cos": np.cos, "tan": np.tan,
  "asin": np.arcsin, "acos": np.arccos, "atan": np.arctan,
  "atan2": np.arctan2, "abs": np.abs}

# calculate value for derivative dy/dx using 
# given expression and supplied arrays of values for x and y
def eval_dyz_dx(x_arr, yz_arr):
    y_arr, z_arr = yz_arr
    global_dict = { "x": x_arr, "y": y_arr, "z":z_arr, "__builtins__": {}}
    global_dict.update(math_fun_dict)
    dy_dx = eval(dy_dx_expr, global_dict)
    dz_dx = eval(dz_dx_expr, global_dict)
    return [dy_dx, dz_dx]

# returns True if a valid expression for f(x,y,z) is given
def test_expr(expr):
    global_dict = { "x": 1.0, "y": 1.0, "z": 1.0, "__builtins__": {}}
    global_dict.update(math_fun_dict)
    try:
        eval(expr, global_dict)
    except:
        valid = False
    else:
        valid = True
    finally:
        return valid

# function returns True if the string is a valid float
def isfloat(x_str):
    try:
        float(x_str)
    except:
        valid = False
    else:
        valid = True
    finally:
        return valid

# function retrieves float number from user
# repeats input if not valid float
def input_float(prompt):
    valid = False
    while valid == False:
        answer = input(prompt)
        valid = isfloat(answer)
        if valid == False:
            print(f"{answer} not a valid float number")
    return(float(answer))

# plot the solution and phase plot
def plot_solution_and_phase_plot():
    # gridspec object defines subplots and their relative size
    gs1 = GridSpec(1, 2, width_ratios=[1, 3], height_ratios=[1])
    title_str = f"{description}\n"
    title_str += f"Differential equations:  dy/dx = {dy_dx_expr},  dz/dx = {dz_dx_expr}\n"
    title_str += f"Initial condition: y({x_start:.1f}) = {y_start},  z({x_start:.1f}) = {z_start}"
    fig = plt.figure(num = title_str, figsize=(16, 9),
                     facecolor = border_color, layout="tight")
    fig.suptitle(title_str, fontsize = text_size + 1, fontweight = "bold")
    plt.subplot(gs1[1])
    # plot solution
    plt.plot(x_arr,y_arr, color = "blue", linewidth = 2, label = "Solution: y = f(x)")
    plt.plot(x_arr,z_arr, color = "red", linewidth = 2, label = "Solution: z = f(x)")
    plt.xticks(fontsize = text_size - 1)
    plt.yticks(fontsize = text_size - 1)
    plt.xlabel("x", fontsize = text_size, fontweight = "bold",)
    plt.ylabel("y, z", fontsize = text_size, fontweight = "bold",)
    plt.grid(True)
    ax = plt.gca()  
    ax.set_facecolor(background_color)
    plt.legend(fontsize = text_size)
    # phase plot
    plt.subplot(gs1[0])
    plt.plot(y_arr, z_arr, color = "blue", linewidth = 2, label = "Phase plot: z = f(y)")
    plt.xticks(fontsize = text_size - 1)
    plt.yticks(fontsize = text_size - 1)
    plt.xlabel("y", fontsize = text_size, fontweight = "bold",)
    plt.ylabel("z", fontsize = text_size, fontweight = "bold",)
    plt.grid(True)
    ax = plt.gca()  
    ax.set_facecolor(background_color)
    plt.legend(fontsize = text_size)

    
# print x, y and z values in table
def print_arr(arr1, arr2, arr3):
    print(f"{"x":<15}|{"y":<15}|{"z":<15}")
    for value1, value2, value3 in zip(arr1, arr2, arr3):
        print(f"{value1:<15.8}|{value2:<15.8}|{value3:<15.8}")

# show constants and functions defined for eval()
def show_functions():
    print("\nThe following constants and functions can be used:")
    for number, item in enumerate(math_fun_dict, 1):
        print(item, end="\t")
        if number % 6 == 0:
            print()
    print()

       
# parameters
text_size = 16
border_color = "#D0D0D0"
background_color = "#F0F0F0"

# take input from user
# try an example or enter own equation and parameters
print("\nCalculate solution to system of two first order ODEs")
print("dy/dx = f(x,y,z)")
print("dz/dx = g(x,y,z)\n")
print("Make your choice:")
print("0 - Enter your own expressions for f(x,y,z) and g(x,y,z)")
for example in examples:
    print(f"{example[0]} - Example: {example[1]}\n     dy/dx = {example[2]}\n     dz/dx = {example[3]}")
valid = False
while valid == False:
    choice = int(input_float(f"\nYour choice, type number 0 to {len(examples)}? "))
    if 0 <= choice <= len(examples):
        valid = True

# process choice made by user
if choice == 0:
    # get inputs
    show_functions()
    dy_dx_expr = input("\ndy/dx = ")
    if test_expr(dy_dx_expr) == False:
        print(f"{dy_dx_expr} is not a valid expression for f(x,y,z)")
        quit()
    dz_dx_expr = input("\ndz/dx = ")
    if test_expr(dz_dx_expr) == False:
        print(f"{dz_dx_expr} is not a valid expression for f(x,y,z)")
        quit()
    x_start = input_float("lowest value of x = ")
    x_stop = input_float("highest value of x = ")
    y_start = input_float("start value of y = ")
    z_start = input_float("start value of z = ")
    description = input("Optionally, type a description to appear in the plot title\nHit enter to skip\n")
    answer = input("number of steps,\n Hit enter for 2000\nn = ")
    if answer == "":
        n_steps = 2000
    else:
        n_steps = int(answer)
else:
    # take values from examples tuple
    n, description, dy_dx_expr, dz_dx_expr, x_start, x_stop, y_start, z_start = examples[choice - 1]
    n_steps = 2000


# summarize equation and parameters
print("\nCalculating solution for following case:")
print(f"{description}")
print(f"dy/dx = {dy_dx_expr}")
print(f"dz/dx = {dz_dx_expr}")
print(f"x ranging from {x_start} to {x_stop}")
print(f"Initial value for y is {y_start}")
print(f"Initial value for z is {z_start}")
print(f"Calculate {n_steps} points\n")

# prepare array of x values
x_arr = np.linspace(x_start, x_stop, n_steps)
    
# calculate solution for ODE
# call scipy solve_ivp() function
result = solve_ivp(eval_dyz_dx, [x_start, x_stop], [y_start, z_start],
                       t_eval = x_arr, method = "LSODA")   

# if calculation not succesfull, show eror message and abort
if result.success == False:
    print(result.message, "\n Aborting due to error")
    quit()

# show message from scipy solve_ivp()    
print("Scipy function gave following message:\n", result.message)

# extract x and y data from result
y_arr = result.y[0]
z_arr = result.y[1]
x_arr = result.t

# optionally print values
answer = input("\nPrint values before plot? y/n ")
if answer.lower() == "y": 
    print_arr(x_arr, y_arr, z_arr)
    input("Press any key to plot")

# plot solution and phase plot
plot_solution_and_phase_plot()

plt.show()

print("\nApplication has finished\n")
