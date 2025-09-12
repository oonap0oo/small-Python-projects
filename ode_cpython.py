# numerically solve differential equation
# dy/dx = f(x,y)
# using scipy
# and draw slope field

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# some examples of ODEs with parameters
# number, f(x,y), x_start, x_stop, y_start
examples = (
            (1, "-y/5", 0.0, 20.0, 10.0),
            (2, "-y/3+x/4", 0.0, 10.0, 5.0),
            (3, "-x*y", 0.0, 3.0, -1.0),
            (4, "sin(x)-y", 0.0, 12.0, 1.0),
            (5, "-sin(y)", 0.0, 15.0, 3.14),
            (6, "5*y-y**2+2*x", 0.0, 3.0, 2.0),
            (7, "sin(x)*cos(3*y)-y/12", 0.0, 24, 2.5)
            )

# functions which van be used in eval()
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
def eval_dy_dx(x_arr, y_arr):
    global_dict = { "x": x_arr, "y": y_arr, "__builtins__": {}}
    global_dict.update(math_fun_dict)
    dy_dx = eval(dy_dx_expr, global_dict)
    return dy_dx

# returns True if a valid expression for f(x,y) is given
def test_expr(expr):
    global_dict = { "x": 1.0, "y": 1.0, "__builtins__": {}}
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

# draw the slope field of dy_dx on the same plot als the solution
# ds**2 = dx**2 + dy**2
# slope = dy/dx
# ds**2 = dx**2 + slope**2 * dx**2
# ds**2 = dx**2 * (1 + slope**2)
# dx = ds / sqrt(1 + slope**2)
# dy = slope * dx
def draw_slope_field():
    nstep = 15
    ds_size = 1.0
    xmin, xmax, ymin, ymax = plt.axis()
    # prepare arrays containing xy coord. for arrows
    x_pos = np.linspace(xmin, xmax, nstep)
    y_pos = np.linspace(ymin, ymax, nstep)
    X, Y = np.meshgrid(x_pos, y_pos)
    # prepare array containing slope at the various points
    SLOPE = eval_dy_dx(X, Y)
    # prepare arrays containing x and y components of arrows
    DX = ds_size / np.sqrt(1 + SLOPE**2)
    DY = SLOPE * DX
    # draw arrows in one go
    ax = plt.gca()
    ax.quiver(X, Y, DX, DY, angles = "xy",
              units = "width", width = 1/800,
              scale_units = "width", scale = 30,
              color = "red", label = "Slope Field - dy/dx")

# plot the solution and call draw_slope_field()
def plot_solution_and_slope_field():
    title_str = f"Differential equation: dy/dx = {dy_dx_expr}\n Initial condition: y({x_start:.1f}) = {y_start}"
    plt.figure(num = title_str, figsize=(16, 10),
               facecolor = border_color, layout="tight")
    plt.title(title_str, fontsize = text_size + 1, fontweight = "bold", y = 1.03)
    # plot solution
    plt.plot(x_arr,y_arr, color = "blue", linewidth = 3, label = "Solution - y=f(x)")
    # draw slope field
    draw_slope_field()
    # plot settings
    plt.xticks(fontsize = text_size - 1)
    plt.yticks(fontsize = text_size - 1)
    plt.xlabel("x", fontsize = text_size, fontweight = "bold",)
    plt.ylabel("y", fontsize = text_size, fontweight = "bold",)
    plt.grid(True)
    ax = plt.gca()  
    ax.set_facecolor(background_color)
    plt.legend(fontsize = text_size)
    
# print x and y values in table
def print_arr(arr1, arr2, prompt = ("","")):
    print(f"{prompt[0]:<15}|{prompt[0]:<15}")
    for value1, value2 in zip(arr1, arr2):
        print(f"{value1:<15.8}|{value2:<15.8}")

# show constants and functions defined for eval()
def show_functions():
    print("\nThe following constants and functions can be used:")
    for number, item in enumerate(math_fun_dict, 1):
        print(item, end="\t")
        if number % 6 == 0:
            print()
    print()

       
# parameters
text_size = 18
border_color = "#D0D0D0"
background_color = "#F0F0F0"

# take input from user
# try an example or enter own equation and parameters
print("\ndy/dx = f(x,y)\n")
print("0 -  Enter expression for f(x,y)")
for example in examples:
    print(f"{example[0]} -  Example :dy/dx = {example[1]}")
valid = False
while valid == False:
    choice = int(input_float(f"\nMake your choice: 0 to {len(examples)}? "))
    if 0 <= choice <= len(examples):
        valid = True

# process choice made by user
if choice == 0:
    # get inputs
    show_functions()
    dy_dx_expr = input("\ndy/dx = ")
    if test_expr(dy_dx_expr) == False:
        print(f"{dy_dx_expr} is not a valid expression for f(x,y)")
        quit()
    x_start = input_float("lowest value of x = ")
    x_stop = input_float("highest value of x = ")
    y_start = input_float("start value of y = ")
    answer = input("number of steps,\n Hit enter for 2000\nn = ")
    if answer == "":
        n_steps = 2000
    else:
        n_steps = int(answer)
else:
    # take values from examples tuple
    n, dy_dx_expr, x_start, x_stop, y_start = examples[choice - 1]
    n_steps = 2000


# summarize equation and parameters
print("\nCalculating solution for following case:")
print(f"dy/dx = {dy_dx_expr}")
print(f"x ranging from {x_start} to {x_stop}")
print(f"Initial value for y is {y_start}")
print(f"Calculate {n_steps} points\n")

# prepare array of x values
x_arr = np.linspace(x_start, x_stop, n_steps)
    
# calculate solution for ODE
# call scipy solve_ivp() function
result = solve_ivp(eval_dy_dx, [x_start, x_stop], [y_start],
                       t_eval = x_arr, method = "LSODA")   

# if calculation not succesfull, show eror message and abort
if result.success == False:
    print(result.message, "\n Aborting due to error")
    quit()

# show message from scipy solve_ivp()    
print("Scipy function gave following message:\n", result.message)

# extract x and y data from result
y_arr = result.y[0]
x_arr = result.t

# optionally print values
answer = input("\nPrint values before plot? y/n ")
if answer.lower() == "y": 
    print_arr(x_arr, y_arr, ("x","y"))
    input("Press any key to plot")

# plot solution and slope field
plot_solution_and_slope_field()

plt.show()

print("\nApplication has finished\n")
