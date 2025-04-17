#!/usr/bin/env python3
#
#  scipy_convolution_sallen_key_lpf_v2.py
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
#  This code defines the transferfunction of an example 
#  VCVS Sallen-Key active analog low pass filter as function of s.
#  It uses the information to: 
#  calculate the impulse response using Scipy function signal.impulse()  
#  calculate the frequency response using scipy function signal.bode()
#  It performs a convolution of the input signals and the impulse response using scipy function signal.convolve()
#  The input signals are a square wave generated using Scipy function signal.square() 
#  and a sawtooth generated using Scipy function signal.sawtooth().
#  Graphs are made using matplotlib. Calculations use numpy arrays.

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

circuit = r"""
            Sallen – Key VCVS Low Pass Filter Circuit
                               C1
              o----------------| |---------------o
              |                                  |
              |                   | -            |
         R1   |   R2              |    -         |
Vin o---/\/\--o--/\/\--o----------|+      -      | 
                       |          |          ----o--o Vout
                      ___     o---|-      -      |
                   C2 ___     |   |    -         |
                       |      |   | -            |
                       |      |                  |
0V o-------------------o      o------------------o
                       |
                      Gnd

 Vout(s)                        1
________  =  ______________________________________  

 Vin(s)        C1.C2.R1.R2.s² + C2.(R1 + R2).s + 1

"""

# this function takes the component value of the Sallen-Key VCVS LPF
# and returns the coefficients of the transfer function in the correct format
# to use with the scipy functions
def get_system_parameters_vcvs_lpf(R1, R2, C1, C2):
    # the numerator and denominator should be 
    # specified in descending exponent order
    # numerator:
    #   1.0 ->  [1]
    # denominator:  
    #   a.s² + b.s + c -> [a, b, c]
    a = C1 * C2 * R1 * R2
    b = C2 * (R1 + R2)
    c = 1.0
    return( ([1.0], [a, b, c]) )


# *** PARAMETERS ****
# System - circuit
R1_Ohm = 30e3
R2_Ohm = 18e3
C1_F = 10e-9
C2_F = 4.7e-9
# input signal
period_input_signal_s = 2e-3
# calculation
time_interval_s = 6e-3
number_of_time_points = 2000
#plots
text_size = 14
color_plot_background = "#F0F0F0"
color_background = "#E0E0E0"
color_fill_between = "#6068D0"
main_title = "Impulse Response and Convolution of an analog filter using Scipy and Python".title()


# print info about the circuit
print(circuit)
print("Component values:")
print(f"R1 = {R1_Ohm / 1e3:.1f} kOhm, R2 = {R2_Ohm / 1e3:.1f} kOhm")
print(f"C1 = {C1_F / 1e-9:.2f} nF, C2 = {C2_F / 1e-9:.2f} nF\n")
# natural frequency
fo = 1 / (2.0 * np.pi * np.sqrt(R1_Ohm * R2_Ohm * C1_F * C2_F))
print(f"Natural frequency: f0 = {fo:.1f} Hz")
# Q factor
Q = np.sqrt(R1_Ohm * R2_Ohm * C1_F * C2_F) / (C2_F * (R1_Ohm + R2_Ohm))
print(f"Q - factor:  Q = {Q:.3f}\n")


# get the system parameters, a tuple of lists containing the coefficients of the transfer function
system_lpf = get_system_parameters_vcvs_lpf(R1_Ohm, R2_Ohm, C1_F, C2_F)
print(f"Numerator coefficients: {system_lpf[0]}")
print(f"Denominator coefficients: {system_lpf[1]}")

# prepare numpy array with time values
t_values = np.linspace(0, time_interval_s, number_of_time_points)

# calculate the impulse response using scipy function signal.impulse()
t, impulse_values = signal.impulse(system_lpf, T = t_values)
# normalise the impulse response
impulse_values /= sum(impulse_values)

# prepare the input signals for the circuit
input_signal_square = signal.square(t_values * (2 * np.pi) / period_input_signal_s )
input_signal_sawtooth = signal.sawtooth(t_values * (2 * np.pi) / period_input_signal_s )

# calculate the output signals using scipy function signal.convolve()
# an output signal is the convolution of the impulse response and input signal
output_signal_square = signal.convolve(input_signal_square, impulse_values)
output_signal_sawtooth = signal.convolve(input_signal_sawtooth, impulse_values)

# calculate the frequency response using scipy function signal.bode()
# w: Frequency array [rad/s]
# mag: Magnitude array [dB]
# phase: Phase array [deg]
w, mag, phase = signal.bode(system_lpf)


# plotting

# use a ms scale for the time axis
t_values_ms = t_values * 1e3

# create new figure object
fig = plt.figure(figsize = (15, 10), num = f"{main_title} - 1", facecolor = color_background)

# overal title
#plt.suptitle(main_title, fontweight = "bold", size = text_size + 3)

# show schematic
plt.subplot(3,3,1)
plt.gca().set_facecolor(color_plot_background) 
plt.xticks([], [])
plt.yticks([], [])
img = np.asarray(Image.open("sallen_key_vcvs_lpf_schematic_2.png"))
plt.imshow(img)
plt.title("Sallen-Key Low Pass Filter", fontsize = text_size, fontweight = "bold")

# plot the impulse response
time_range = len(t_values_ms) // 3
plt.subplot(3,3,2)
plt.gca().set_facecolor(color_plot_background) 
plt.plot(t_values_ms[:time_range], impulse_values[:time_range], color = "green", linewidth = 2.5)
plt.fill_between(t_values_ms[:time_range], impulse_values[:time_range], label = "Impulse response of analog filter", color = "green", alpha = 0.15)
plt.legend(fontsize = text_size - 1)
plt.grid(visible = True)
plt.xlabel("t [ms]", fontsize = text_size)
plt.ylabel("f(t)", fontsize = text_size)
plt.tick_params(labelsize = text_size)
plt.title("Impulse response\nUsing Scipy function signal.impulse()", fontsize = text_size, fontweight = "bold")


# plot frequency response
plt.subplot(3,3,3)
plt.gca().set_facecolor(color_plot_background) 
plt.semilogx(w / 1e3 / 2.0 / np.pi, mag, linewidth = 2.5, label = "Magnitude [dB]")
plt.legend(fontsize = text_size - 1)
plt.grid(visible = True)
plt.xlabel("f [kHz]", fontsize = text_size)
plt.ylabel("Magnitude,[dB]", fontsize = text_size)
plt.tick_params(labelsize = text_size)
plt.title("Frequency response, magnitude\nUsing Scipy function signal.bode()", fontsize = text_size, fontweight = "bold")


# plot input and output signals
plt.subplot(3,1,2)
plt.gca().set_facecolor(color_plot_background) 
plt.plot(t_values_ms, input_signal_square, color = color_fill_between, linewidth = 2.5)
plt.fill_between(t_values_ms, input_signal_square, label = "Input signal", color = color_fill_between, alpha = 0.15)
plt.plot(t_values_ms, output_signal_square[0:len(input_signal_square)], label = "Output signal", color = "red", linewidth = 2.5)
plt.grid(visible = True)
plt.xlabel("t [ms]", fontsize = text_size)
plt.ylabel("f(t)", fontsize = text_size)
plt.legend(fontsize = text_size - 1)
plt.tick_params(labelsize = text_size)
plt.title("Square wave and reaction of circuit\nConvolution of square wave with impulse response using scipy function signal.convolve()", fontsize = text_size, fontweight = "bold")

plt.subplot(3,1,3)
plt.gca().set_facecolor(color_plot_background) 
plt.plot(t_values_ms, input_signal_sawtooth, color = color_fill_between, linewidth = 2.5)
plt.fill_between(t_values_ms, input_signal_sawtooth, label = "Input signal", color = color_fill_between, alpha = 0.15)
plt.plot(t_values_ms, output_signal_sawtooth[0:len(input_signal_sawtooth)], label = "Output signal", color = "red", linewidth = 2.5)
plt.grid(visible = True)
plt.xlabel("t [ms]", fontsize = text_size)
plt.ylabel("f(t)", fontsize = text_size)
plt.legend(fontsize = text_size - 1)
plt.tick_params(labelsize = text_size)
plt.title("Sawtooth and reaction of circuit\nConvolution of sawtooth with impulse response using scipy function signal.convolve()", fontsize = text_size, fontweight = "bold")


# define space between subplots
plt.subplots_adjust(wspace = 0.236, hspace = 0.583, left = 0.05, right = 0.98, bottom = 0.062, top = 0.936)

# start with plot window maximized, this works at least in linux..
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())


plt.show()
