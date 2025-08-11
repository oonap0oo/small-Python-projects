# Nyquist, Bode and Nichols plot of control loop with PID controller
#
#   Control loop with negative feedback, PID controller and process
#
#                  e           u
#          +       |           |
#   r ------o------+--| PID |--+--| PROCESS |---+----y
#          -|                                   |
#           |                                   |
#           |                                   |
#           -------------------------------------
#
#       e = r - s
#
#   Nyquist, Bode and Nichols plots made of OPEN loop gain:
#
#   OPEN loop gain = PID(s) * PROCESS(s) = y(s) / e(s)
#

import numpy as np
import matplotlib.pyplot as plt

# pid controller
def pid(s, Kp, Ti, Td):
    pid_output = Kp * ( 1 + 1/(Ti*s) + Td*s )
    return pid_output

# process systems
# 1e order linear system
# Kp: gain
# Tc: time constant
def system_1_order(s, Kp, Tc):
    system_gain = K1 / ( 1 + Tc*s ) 
    return system_gain

# 2nd order linear system
# Kp: gain
# Tc: time constant
# Zd: damping factor
def system_2_order(s, Kp, Tc, Zd):
    system_gain = Kp / ( Tc**2 * s**2 + 2 * Zd * Tc * s + 1 )
    return system_gain

# time delay
# Tdelay: time delay in seconds
def system_time_delay(s, Tdelay):
    system_gain = np.exp(-Tdelay * s)
    return system_gain

# process consisting of 1e order, 2nd order linear systems and time delay
def process(s):
    process_gain = system_1_order(s, K1, T1) * system_2_order(s, K2, T2, Z2) * system_time_delay(s, Tdelay) 
    return process_gain

# calculate pid, process and total open loop gain ifo. frequency
# and store results in numpy arrays
def calc_nyquist_data(f_start, f_stop, number_points):
    # s is array of complex frequency, using logaritic spacing
    s_arr = 1j * 2.0 * np.pi * np.logspace(np.log10(f_start), np.log10(f_stop), num = number_points)
    # arrays of values of transferfunction of process, pid  and total open loop gain
    process_arr = process(s_arr)
    pid_arr = pid(s_arr, Kp, Ti, Td)
    open_loop_gain_arr = pid_arr * process_arr
    return (s_arr, open_loop_gain_arr, process_arr, pid_arr)

# show Nyquist plot, polar plot of open loop gain
# also process and pid transfer functions shown
def show_nyquist_plot(open_loop_gain_arr, process_arr, pid_arr):
    plt.figure(figsize = (15, 9), num = "Nyquist plot of control loop", facecolor = color_background)
    plt.polar(np.angle(open_loop_gain_arr), np.abs(open_loop_gain_arr),
              color = "red", label = "Open loop gain", linewidth = 2)
    plt.polar(np.angle(process_arr), np.abs(process_arr),
              color = "green", label = "Process", linewidth = 2, linestyle='--')
    plt.polar(np.angle(pid_arr), np.abs(pid_arr),
              color = "orange", label = "PID controller", linewidth = 2, linestyle='--')
    plt.polar(np.pi, 1.0, marker = "o", color = "black", markersize = 10, label = "-1")
    ax=plt.gca()
    ax.set_rlim(0, max_magnitide_polar_plot)
    ax.set_facecolor(color_plot_background) 
    plt.grid(True)
    plt.tick_params(labelsize = text_size)
    plt.legend(fontsize = text_size)
    plt.title(f"Nyquist plot of control loop\nGain margin = {gain_margin:.3} dB, Phase margin = {np.degrees(phase_margin):.2f}°",
              fontsize = text_size + 1, fontweight = "bold", y = 1.05)

# show Bode plot, plot of open loop gain magnitude and phase ifo. frequency
# also process and pid transfer functions shown
def show_bode_plot(s_arr, open_loop_gain_arr, process_arr, pid_arr):
    f_arr = s_arr.imag / (2 * np.pi)
    fig = plt.figure(figsize = (15, 9), num = "Bode plot of control loop", facecolor = color_background)
    fig.suptitle(f"Bode plot of control loop\nGain margin = {gain_margin:.3} dB, Phase margin = {np.degrees(phase_margin):.2f}°",
                 fontsize = text_size + 1, fontweight = "bold", y = 0.98)
    plt.subplot(211)
    plt.semilogx(f_arr, 20 * np.log10(np.abs(open_loop_gain_arr)), linewidth = 2,color = "red",
                 label = "Open loop gain")
    plt.semilogx(f_arr, 20 * np.log10(np.abs(process_arr)), color = "green", linewidth = 2, linestyle='--',
                  label = "Process")
    plt.semilogx(f_arr, 20 * np.log10(np.abs(pid_arr)), color = "orange", linewidth = 2, linestyle='--',
                  label = "PID controller")
    plt.semilogx((f_arr[0], f_arr[-1]), (0.0, 0.0), color = "black", linewidth = 2, linestyle=':',
                  label = "0dB")
    plt.xlabel("Frequency [Hz]", fontsize = text_size)
    plt.ylabel("Gain [dB]", fontsize = text_size)
    plt.grid(True)
    plt.tick_params(labelsize = text_size)
    plt.legend(fontsize = text_size)
    plt.subplot(212)
    plt.semilogx(f_arr, np.degrees(np.unwrap(np.angle(open_loop_gain_arr))), linewidth = 2,color = "red",
                 label = "Open loop gain")
    plt.semilogx(f_arr, np.degrees(np.unwrap(np.angle(process_arr))), color = "green", linewidth = 2, linestyle='--',
                  label = "Process")
    plt.semilogx(f_arr, np.degrees(np.unwrap(np.angle(pid_arr))), color = "orange", linewidth = 2, linestyle='--',
                  label = "PID controller")
    plt.semilogx((f_arr[0], f_arr[-1]), (-180.0, -180.0), color = "black", linewidth = 2, linestyle=':',
                  label = "-180°")
    plt.xlabel("Frequency [Hz]", fontsize = text_size)
    plt.ylabel("Angle [°]", fontsize = text_size)
    plt.grid(True)
    plt.tick_params(labelsize = text_size)
    plt.legend(fontsize = text_size)

# show Nichols plot, plot of open loop gain magnituse ifo. phase 
# also process and pid transfer functions shown
def show_nichols_plot(open_loop_gain_arr, process_arr, pid_arr):
    fig = plt.figure(figsize = (15, 9), num = "Nichols plot of control loop", facecolor = color_background)
    plt.title(f"Nichols plot of control loop\nGain margin = {gain_margin:.3} dB, Phase margin = {np.degrees(phase_margin):.2f}°",
                 fontsize = text_size + 1, fontweight = "bold", y = 0.98)
    plt.plot(np.degrees(np.unwrap(np.angle(open_loop_gain_arr))),
             20 * np.log10(np.abs(open_loop_gain_arr)),
             linewidth = 2,color = "red", label = "Open loop gain")
    plt.plot(np.degrees(np.unwrap(np.angle(process_arr))),
             20 * np.log10(np.abs(process_arr)),
             linewidth = 2,color = "green", linestyle='--', label = "Process")
    plt.plot(np.degrees(np.unwrap(np.angle(pid_arr))),
             20 * np.log10(np.abs(pid_arr)),
             linewidth = 2,color = "orange", linestyle='--', label = "PID controller")
    plt.plot(-180.0, 0.0, marker = "o", color = "black", label = "-1.0")
    plt.xlabel("Phase angle [°]", fontsize = text_size)
    plt.ylabel("Gain [dB]", fontsize = text_size)
    plt.grid(True)
    plt.tick_params(labelsize = text_size)
    plt.legend(fontsize = text_size)

# phase margin?
def get_phase_margin(open_loop_gain_arr):
    diff_arr = np.abs(np.abs(open_loop_gain_arr) - 1.0)
    index = diff_arr.argmin()
    phase_margin = np.pi + np.angle(open_loop_gain_arr[index])
    print(f"Phase margin = {np.degrees(phase_margin):.2f}°")
    return phase_margin

# gain margin?
def get_gain_margin(open_loop_gain_arr):
    diff_arr = np.abs(np.angle(open_loop_gain_arr) + np.pi)
    index = diff_arr.argmin()
    gain_margin = -20 * np.log10( np.abs(open_loop_gain_arr[index]) )
    print(f"Gain margin = {gain_margin:.3} dB")
    return gain_margin

# set numerical values for pid and process parameters as example

# pid controller
Kp = 4.0 # gain proportional term of PID controller
Ti = 5.0 # integration time constant of PID controller
Td = 1.0 # derivative time constant of PID controller

# 1e order linear system
K1 = 1.0 # gain &nd order process
T1 = 0.5 # time constant &nd order process

# 2nd order linear system
K2 = 2.0 # gain 2nd order process
T2 = 2.0 # time constant 2nd order process
Z2 = 0.7 # damping 2nd order process

# time delay
Tdelay = 0.2 # time delay

# parameters of calculation
f1 = 0.001 # lowest frequency used
f2 = 3 # highest frequency used
N = 300 # number of data points calculated

# parameters ofplotting
max_magnitide_polar_plot = 3 # scale maximum r value 
text_size = 16
color_plot_background = "#F8F8F8"
color_background = "#E0E0E0"
colors_plot = ("#150086","#86001E","#008611")

# calculate nyquist data
s_arr, open_loop_gain_arr, process_arr, pid_arr = calc_nyquist_data(f1, f2, N)

# phase and gain margin
phase_margin = get_phase_margin(open_loop_gain_arr)
gain_margin = get_gain_margin(open_loop_gain_arr)

# show plots
show_nyquist_plot(open_loop_gain_arr, process_arr, pid_arr)
show_bode_plot(s_arr, open_loop_gain_arr, process_arr, pid_arr)
show_nichols_plot(open_loop_gain_arr, process_arr, pid_arr)

plt.show()











