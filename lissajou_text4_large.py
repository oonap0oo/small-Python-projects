# lissajou in text format

# text has to be send line per line
# code has to work out which x values are part of the lissajou curve
# for each succesive y value (or line to be send)

# lissajou with twi relatibe freq. and a phase shift
# x(t) = x_ampl * cos(fx * t)
# y(t) = y_ampl * sin(fy * t + phase)

# calculating parameter t values at given y 
# sin(fy * t + phase) = y(t) / y_ampl
# => fy * t1 + phase = asin(y(t) / y_ampl) + k * 2 * pi
# => t1 = 1/fy * ( asin(y(t) / y_ampl) + k * 2 * pi - phase ) 
# => fy * t2 + phase = pi - asin(y(t) / y_ampl) - k * 2 * pi = pi * (1 - 2 * k) - asin(y(t) / y_ampl)
# => t2 = 1/fy * ( - asin(y(t) / y_ampl) + (1 - 2 * k) * pi - phase )

# parameter t values at given y, k is an integer number
# t1(y, k) = 1/fy * ( asin(y(t) / y_ampl) + k * 2 * pi - phase )
# t2(y, k) = 1/fy * ( - asin(y(t) / y_ampl) + (1 - 2 * k) * pi - phase )

from math import *

# parameters lissajou
fx = 3; fy = 5 # relative frequencies for x and y
phase = pi/9 # phase shift of y versus x

# parameters plotting
char = "⏺" # character used for plot
axes_char = "⬩" # character used for axes
x_ampl = 80; y_ampl = 20 # x and y amplitudes given in number of characters

# function to calculate x out of parameter t
def calculate_x(t):
    return int( x_ampl * ( 1.0 + 0.96 * cos(fx * t)) + .5)

# text header
print("  Lissajou")
print(f"  x(t) = {x_ampl} * cos({fx} * t)")
print(f"  y(t) = {y_ampl} * sin({fy} * t + {phase:.3f})\n")

# for each y value: calculate x values and plot
N_k = max(fx, fy) # number of values for x at any given y depends on relative frequencies
for y in range(-y_ampl, y_ampl + 1): # looping through all values for y
    # prepare list of characters "line" which will become next output 
    if y == 0:
        line = [axes_char] * (2 * x_ampl) # draw x axis
    else:
        line = [" "] * (x_ampl) + [axes_char] + [" "] * (x_ampl-1) # draw y axis
    # calculating all x values at the current y and inserting plot markers in "line"
    for k in range(N_k):
        t1 = 1/fy * ( asin(y / y_ampl) + k * 2 * pi  - phase ) 
        line[ calculate_x(t1) ] = char
        t2 = 1/fy * ( -asin(y / y_ampl) + (1 - 2 * k) * pi  - phase ) 
        line[ calculate_x(t2) ] = char        
    # convert list "line" to string and print
    print("".join(line))

        
    
