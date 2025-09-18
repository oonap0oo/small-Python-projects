# Chua circuit using equations for physical circuit

# Circuit
# -------
#G is a piecewise linear
# negative resistance implemented using opamp(s)
# it supplies energy to the circuit and provides gain and non linearity
#
#     il       v2                      v1      iG
# +--->---------+---------- R ---------+------->------+
# |             |                      |              |    
# |             v iC2                  v iC1          |    
# |             |                      |              |    
# L             C2                     C1             G   
# |             |                      |              |
# |             |                      |              |
# |             |                      |              |    
# +-------------+----------------------+--------------+---o Gnd
#
# iC2 = C2*dv2/dt,   iC1 = C1*dv1/dt,   v2 = -L*dil/dt
# sum of currents into node is zero:
# iC1 = (v2 - v1) / R - iG
# iC2 = il + (v1 - v2) / R
# The current iG is a function of voltage across G which is v1
# iG = f(v1)
# combining above gives system of ODEs:
#
# System of Differential equations
# --------------------------------
# 
# C1*dv1/dt = 1/R * (v2 - v1) - f(v1)
# C2*dv2/dt = 1/R * (v1 - v2) + il
# L*dil/dt = -v2 - rs * il
#
# v1: voltage across C1
# v2: voltage across C2
# il: current throught L
# f: current through piecewise linear
#    negative resistance G
#
# a circuit implementation also simulated in LTspice:
#
#                             2                6
#                             +---- 290 Ohm ---+
#                             |                |
#                             +---------> +    |
#                             |           VCVS E = 1.241
#                             |      +--> -    |    
#                             |      |         |    
#                             |      +---+-----+------o Gnd
#                             |
#                             |
#                             |           o +9V
#                             |           |
#                             |           47K
#        1            2       |           |
# +------+---- R1 ----+-------+------>|---+-- 3K3 ----o Gnd
# |      |            |       |      
# |      |            |       +------|<---+-- 3K3 ----o Gnd      
# |      |            |                   |     
# |      |            |                   47K
# L1     C2           C1                  |
# |      |            |                   o -9V
# |      |            |     
# |      |            |     
# |      |            |     
# +------+------------+---------o Gnd
#
# ^^^ Resonance LC circuit ^^^    
#                             ^^^ non linear negative impedance ^^^                                   
#
# Derive the I=f(V) characteristic of piece wise linear negative resistance G
#
# Around VCVS E:
# V6 = 1.241 * V2
# Current throught 290 Ohm:
# I = (V6-V2)/290 = V2*(1.241-1)/290 = V2*831.0e-06
# G1 = -I/V2 = -831.0e-06 1/Ohm = -1 / (1203 Ohm)
# so G1 is approx. -800 1/Ohm
# If diodes do not conduct, voltage across 3K3 resistors:
# v(3k3) = 3.3/(3.3+47)*(+-9V) = +-0.59V
# diodes conduct if
# V2 > vdiode + 0.59V approx. 1.2V
# V2 < -vdiode - 0.59V approx. -1.2V
# If diodes conduct, extra load seen:
# 3k3 // 47k = 1/(1/3300+1/47e3) = 3083 Ohm
# combination G1 and extra resistor load:
# Z2 = (1/G1) // 3083 Ohm = 1/(-831.0e-06 1/Ohm + 1/3083 Ohm)
# Z2 = -1973.8 Ohm = -1/(506.6e-06 Ohm)
# G2 = 1/Z2 = -506.6e-06 1/Ohm
# so G2 is approx. -500e-6 1/Ohm
#
# Current through G ifo. voltage across G
# ---------------------------------------
#
#             +         . I(G)=f(v)
#                +      .
#                   +   .
#                    +  .
#                     + .
#                      +.    1.2V 
# ..........................+................ v
#                       .+  . 
#                       . + . I/V = G1 = -800e-6 1/Ohm
#                       .  +.
#                       .   +
#                       .      +
#                       .         + I/V = G2 = -500e-6 1/Ohm
#                       .            +

import numpy as np # vectorized calculations
import matplotlib.pyplot as plt # plotting
from scipy.integrate import solve_ivp # function to solve system of ODEs


# defines piecewise negative resistance of "Chua diode"
# often implemented physically using opamp(s)
G1 = -800e-6 # 1/Ohm negative conductance if v > 1.2 or v < -1.2
G2 = -500e-6 # 1/Ohm negative conductance if 1.2 <= v 1.2
def f(v):
   return np.piecewise(v, [v < -1.2, v >= -1.2, v > 1.2],
                       [lambda x: G2*x+1.2*(G2-G1),
                        lambda x: G1*x,
                        lambda x: G2*x+1.2*(G1-G2)])

# defines system of differential equations
# for physical Chua circuit with component values
def chua(t, var):   
    v1, v2, il = var
    # differential equations using
    # i=C*dv/dt and v=L*di/dt
    dv1_dt = 1/C1 * ( 1/R * (v2 - v1) - f(v1) )  
    dv2_dt = 1/C2 * ( 1/R * (v1 - v2) + il )
    dil_dt = 1/L * ( -v2 - 0.1 * il ) # adding some series resistance for L 
    return [dv1_dt, dv2_dt, dil_dt]
   

# **** parameters *******************

# parameters calculation                    
T = 25e-3 # total time in s
N = 4000 # number of points saved

# parameters chua system        
R = 1600
C1 = 4.6E-9
C2 = 47E-9
L = 8.5E-3

# intial conditions
v1_0 = 0.7
v2_0 = 0
il_0 = 0

# parameters for the plots
title = f"Chua's circuit using differential equations describing physical circuit"
text_size = 14
color_plot_background = "black"
color_background = "black"
colors_plot = ("#00D000","#00D000","#00D000") 
color_grid = "#505050"
fov_3d_deg = 110 # field of view in degrees which controlles the perspective rendering of 3D plot

# **** calculation ************************

print("\n" + title)
print("-" * len(title))
print("Starting scipy function solve_ivp()")

# prepare an array of time points at which values have to be returned by the scipy function
t = np.linspace(0, T, N)

# calculating solution of system of differential equations decribed by python function chua()
# the method had to be changed from the default "RK45" for usable calculation
result = solve_ivp(chua, (0, T),
                   [v1_0, v2_0, il_0], t_eval = t,
                   method = "LSODA")

# some text feedback for console
print(result)

# if calculation unsuccesful, abort here
if result.success == False:
    quit()

# unpack values from result object
v1, v2, il = result.y

# generate data to show i=f(v) graph of G
v_G = np.linspace(-3,3,150)
i_G = f(v_G)

# **** plotting using matplotlib ***************

# import modules for plotting
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec # align subplots also with variable size

# use white elements on black background
plt.style.use('dark_background')

# set grid color fpr all plots
plt.rcParams['grid.color'] = color_grid


# create new figure object for graph of i=f(v) of G
fig = plt.figure(figsize = (10, 10), num = "'Chua diode', piecewise linear negative resistance", facecolor = color_background)

ax = fig.add_subplot()
ax.grid(linestyle='-')
ax.set_facecolor(color_plot_background)
ax.set_xlabel("voltage [V]", size = text_size, fontweight = "bold")
ax.set_ylabel("current [mA]", size = text_size, fontweight = "bold")
ax.plot(v_G, i_G * 1e3, color = colors_plot[0])
ax.set_title("current vs voltage of 'Chua diode'", fontweight = "bold", size = text_size)

# create new figure object for graph of v=(t), i=f(t)
fig = plt.figure(figsize = (15, 10), num = "Chua's circuit, plots vs time", facecolor = color_background)

# overal title
plt.suptitle(title, fontweight = "bold", size = text_size + 4)

ax = fig.add_subplot(311)
ax.grid(linestyle='-')
ax.set_facecolor(color_plot_background)
ax.set_xlabel("time", size = text_size, fontweight = "bold")
ax.set_ylabel("voltage[V]", size = text_size, fontweight = "bold")
ax.plot(result.t, v1, color = colors_plot[0])
ax.set_title("v1 vs time", fontweight = "bold", size = text_size)

ax = fig.add_subplot(312)
ax.grid(linestyle='-')
ax.set_facecolor(color_plot_background)
ax.set_xlabel("time", size = text_size, fontweight = "bold")
ax.set_ylabel("voltage[V]", size = text_size, fontweight = "bold")
ax.plot(result.t, v2, color = colors_plot[0])
ax.set_title("v2 vs time", fontweight = "bold", size = text_size)

ax = fig.add_subplot(313)
ax.grid(linestyle='-')
ax.set_facecolor(color_plot_background)
ax.set_xlabel("time", size = text_size, fontweight = "bold")
ax.set_ylabel("current [mA]", size = text_size, fontweight = "bold")
ax.plot(result.t, il * 1e3, color = colors_plot[0])
ax.set_title("il vs time", fontweight = "bold", size = text_size)

# define space between subplots
plt.subplots_adjust(wspace = 0, hspace = 0.35, left = 0.048, right = 0.981, bottom = 0.062, top = 0.898)

# start with plot window maximized, this works at least in linux..
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

# gridspec object defines subplots and their relative size
gs = GridSpec(2, 2, width_ratios=[1, 3], height_ratios=[1, 1])

# create new figure object for xy plots of circuit voltages and current
fig = plt.figure(figsize = (15, 10), num = "Chua's circuit, xy and 3D plots", facecolor = color_background)

# overal title
plt.suptitle(title, fontweight = "bold", size = text_size + 4)

# add subplot for v2 vs v1 values
ax = fig.add_subplot(gs[0])
ax.grid(linestyle='-')
ax.set_facecolor(color_plot_background)
ax.set_xlabel("v1", size = text_size, fontweight = "bold")
ax.set_ylabel("v2", size = text_size, fontweight = "bold")
ax.plot(v1,v2, color = colors_plot[0])
ax.set_title("Values of v2 vs v1", fontweight = "bold", size = text_size)

# add subplot for v2 vs il values
ax = fig.add_subplot(gs[2])
ax.grid(linestyle='-')
ax.set_facecolor(color_plot_background)
ax.set_xlabel("il", size = text_size, fontweight = "bold")
ax.set_ylabel("v2", size = text_size, fontweight = "bold")
ax.plot(il, v2, color = colors_plot[1])
ax.set_title("Values of v2 vs il", fontweight = "bold", size = text_size)

# for 3D plot: calculate focal length out of field of view
focal_len = 1 / np.tan(np.radians(fov_3d_deg / 2))
#print(f"focal length for 3D plot: {focal_len:.8} for a field of view of {fov_3d_deg}°")

# add subplot for 3D scatter plot of v1,v2,il
ax = fig.add_subplot(gs[:,1],projection = "3d")
ax.set_proj_type('persp', focal_length=focal_len)
ax.plot(v1, v2, il, color = colors_plot[2])
ax.set_facecolor(color_plot_background)
ax.set_xlabel("v1", size = text_size, fontweight = "bold")
ax.set_ylabel("v2", size = text_size, fontweight = "bold")
ax.set_zlabel("il", size = text_size, fontweight = "bold")
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.set_title("3D plot of il VS v1,v2", fontweight = "bold", size = text_size)

# define space between subplots
plt.subplots_adjust(wspace = 0, hspace = 0.229, left = 0.048, right = 0.981, bottom = 0.062, top = 0.898)

# start with plot window maximized, this works at least in linux..
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

plt.show()  

