#!/usr/bin/env python3
#
#  fourier_series_v4.py
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
#  This code calculates the coefficients of the Fourier Series of a number
#  of functions. Each function is plotted with approximations using several numbers 
#  of coefficients. Also the Fourier Series coefficients themselves are plotted.

import numpy as np # library numpy for vectorised calculations
from scipy import integrate, signal # using quad() from scipy.integrate and several waveforms from scipy.signal
import matplotlib.pyplot as plt # plots made using matplotlib
from matplotlib.gridspec import GridSpec # align subplots also with variable size

# a sawtooth function able to accept a numpy array as argument
def sawtooth(x, period, amplitude = 1.0):
    return(amplitude * signal.sawtooth(x * 2 * np.pi / period))

# a square wave function able to accept a numpy array as argument
def square_wave(x, period, amplitude = 1.0):
    return(amplitude * signal.square(x * 2 * np.pi / period))
    
# a pulse function able to accept a numpy array as argument
def pulse(x, period, amplitude = 1.0):
    return(amplitude * (1 + signal.square(x * 2 * np.pi / period, duty = 1/4)) / 2)
    
# a half sine function able to accept a numpy array as argument
def half_sine(x, period, amplitude = 1.0):
    return(amplitude * np.sin(2 * np.pi * x) * ((x % period) < 0.5))
    
# a chopped sine function able to accept a numpy array as argument
def chopped_sine(x, period, amplitude = 1.0):
    return( amplitude * np.sin(2 * np.pi * x) * ((x % (period / 2))  > 0.25) )
    
# a absulute value sine function able to accept a numpy array as argument
def absolute_value_sine(x, period, amplitude = 1.0):
    return(amplitude * np.abs( np.sin(2 * np.pi * x)))
    

# this function calculates a number of a and b coefficients for the Fourier Series
# it takes a function as argument als well as the period to be used
# and the number of coefficients to be calculated
# it returns two numpy arrays containing the a and b coefficients
def calc_fourier_coefficients(fun, period, number_coeff):
    # prepare the two numpy arrays which will be returned
    a = np.zeros(number_coeff)
    b = np.zeros(number_coeff)
    # use the scipy function guad() to calculate integral for coefficient a0
    integral = integrate.quad(fun, 0, period, args = (period, 1.0))
    a[0] = 2 / period * integral[0]
    # calculate the other coefficents
    for n in range(1, number_coeff):
        fun_cos = lambda x: fun(x, period) * np.cos(2 * np.pi * n * x / period)
        integral = integrate.quad(fun_cos, 0, period)
        a[n] =  2 / period * integral[0]
        fun_sin = lambda x: fun(x, period) * np.sin(2 * np.pi * n * x / period)
        integral = integrate.quad(fun_sin, 0, period)
        b[n] =  2 / period * integral[0]
    return(a, b)
    
    
# this function takes the fourier series coefficients a and b, it calculates the approximation of
# the function at points specified by numpy array x
# it returns a numpy array containing the function values    
def fun_sum_of_foerier_terms(a, b, x, period):
    #value = a[0] / 2.0
    value = np.full(x.shape, a[0] / 2.0)
    number_coeff = len(a)
    for n in range(1, number_coeff):
        value += a[n] * np.cos(2 * np.pi * n * x / period) + b[n] * np.sin(2 * np.pi * n * x / period)
    return(value)


# this function generates a series of plots showing several functions and their fourier series approximations
# approximations are show using a increasing number of coefficients
# also the a and b coefficients themselves are plottted
def calculate_and_plot(functions_to_use, number_of_window):
    # gridspec object defines subplots and their relative size
    gs = GridSpec(len(functions_to_use), 2, width_ratios=[3, 1], height_ratios=[1] * len(functions_to_use))
    
    # create new figure object
    fig = plt.figure(figsize = (15, 10), num = f"{main_title} - {number_of_window}", facecolor = color_background)
    
    # overal title
    plt.suptitle(main_title, fontweight = "bold", size = text_size + 2)
    
    for func_number, func in enumerate(functions_to_use):
        
        # calculate the coefficients a and b for the fourier series
        coeff_a, coeff_b = calc_fourier_coefficients(func, period_waveform, total_number_coeff)
        
        # print the coefficients as a table
        print(f"\n function {func.__name__}:")
        print(f"{"n":>10}\t{"a[n]":>10}\t{"b[n]":>10}")
        for n, ab in enumerate( zip(coeff_a, coeff_b) ):
            print(f"{n:>10}\t{ab[0]:>10.3e}\t{ab[1]:>10.3e}")
            
        # create numpy vector with values for independant variable x 
        x_values = np.linspace(0, x_axis_interval, number_of_points)
        
        # calculate the true function values for all x
        fun_values = func(x_values, period_waveform)
        
        # calculate the fourier series approximation using coefficients a and b
        list_fourier_approx = []
        for number_coeff in range(lowest_number_coeff, total_number_coeff + 1, step_number_coeff):
            fourier_approx_values = fun_sum_of_foerier_terms(coeff_a[0:number_coeff], coeff_b[0:number_coeff], x_values, 1.0)
            list_fourier_approx.append( (number_coeff, fourier_approx_values) )
        
        # plotting functions and approximations
        plt.subplot( gs[func_number * 2] )
        plt.gca().set_facecolor(color_plot_background) 
        plt.plot(x_values, fun_values, color = color_fill_between, linewidth = 1.5)
        plt.fill_between(x_values, fun_values, label = f"function {func.__name__}", alpha = 0.15, color = color_fill_between)
        for fourier in list_fourier_approx:
            plt.plot(x_values, fourier[1], label = f"using {fourier[0]} coefficients", linewidth = 2.5)
        #plt.xlabel("x", fontsize = text_size)
        plt.ylabel("f(x)", fontsize = text_size)
        plt.legend(fontsize = text_size - 1)
        plt.tick_params(labelsize = text_size)
        plt.title(f"Fourier approximation of {func.__name__}", fontsize = text_size, fontweight = "bold")
        plt.grid(visible = True)
        
        # plotting the coefficients a and b
        plt.subplot( gs[func_number * 2 + 1] )
        plt.gca().set_facecolor(color_plot_background) 
        nlabels = [f"{n}" for n in range(0, total_number_coeff)]
        plt.bar(nlabels, coeff_a, width = 0.25, align = "edge", label="a coefficients")
        plt.bar(nlabels, coeff_b, width = -0.25, align = "edge", label="b coefficients")
        plt.xlabel("n", fontsize = text_size)
        plt.ylabel("an, bn", fontsize = text_size)
        plt.legend(fontsize = text_size - 1)
        plt.tick_params(labelsize = text_size)
        plt.grid(visible = True)
    
    # define space between subplots
    plt.subplots_adjust(wspace = 0.13, hspace = 0.3, left = 0.05, right = 0.98, bottom = 0.07, top = 0.91)
    
    # start with plot window maximized, this works at least in linux..
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())


# parameter central
total_number_coeff = 15 
step_number_coeff = 5
lowest_number_coeff = 5
period_waveform = 1.0
x_axis_interval = 2.2
number_of_points = 1000
text_size = 14
main_title = "fourier series approximation".title()
color_plot_background = "#F0F0F0"
color_background = "#E0E0E0"
color_fill_between = "#6068D0"

#  generate first plot window with 3 functions
calculate_and_plot((square_wave, pulse, sawtooth), 1)

# generate second plot window with 3 function
calculate_and_plot((absolute_value_sine, chopped_sine, half_sine), 2)

plt.show()

