
#       Buffon's needle
#
#      |<----- D ------>|
#      |                |
#      | θ /            |
#      |--/  length = L |
#      | /              |
#      |/               |
#      X                |
#     /|                |
#      |                |
#      |                |
#
#            2     L
#       p = --- . ---
#            π     D
#
#       D > L
#
#       p: probability needle touches a line
#       L: lenght needle
#       D: distance between lines
#
#       needle touches line if
#
#       s =< x
#
#       x: projection distance from center needle to tip
#       s: distance between center of needle and nearest line
#
#            L
#       x = --- . sin( θ )
#            2
#
#       θ (theta): angle between needle and lines
#
#       p ≈ Ntouches / Ntotal
#
#                 Ntotal      L
#       π ≈ 2 . ---------- . ---
#                Ntouches     D

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec # align subplots also with variable size

# this function returns the projection distance from center of a needle to the tip 
def calculate_x(length_needle, theta):
    return(0.5 * length_needle * np.sin(theta))

# this function returns the approximation of pi
def approximate_pi(total_runs, number_of_touches, length_needle, distance_lines):
    return( 2 * total_runs * length_needle / (number_of_touches * distance_lines) )
    
# parameters
L = 2 # length of the needles
D = 3 # distance between lines, D > L
Nruns = 100 # number of sets of iterations
N = 1000 # number of iterations in each set
# parameters for the plots
text_size = 16
color_plot_background = "#F8F8F8"
color_background = "#E0E0E0"
colors_plot = ("#1f77b4", "#ff7f0e", "#46A1E0")

# creating a numpy ramdon generator
rng = np.random.default_rng() 
# number of needles touching a line summed across the sets
Ntouches_accumulated = 0 
# numpy array which will be filled with successive approximations of pi
pi_approximation_array = np.zeros(Nruns)
 # numpy array which will hold the number of needles touching a line in each set
Ntouches_array = np.zeros(Nruns) 
# numpy array which will keep the accumuated number of runs as sets are processed
Ntotal_array = np.zeros(Nruns) 
# loop which completes all sets of runs
for block in range(Nruns):
    # array containing uniformly random angles theta
    theta_array = rng.uniform(0, np.pi / 2, N)
    # create array which has correspodning distances x for each theta
    x_array = calculate_x(L, theta_array)
    # array containing uniformly random distances s (center of needle to closest line)
    s_array = rng.uniform(0, D / 2, N)
    # count how many needles touch a line and store that number in array
    Ntouches_array[block] = np.count_nonzero( s_array <= x_array )
    # keep track of total number of needles processed in each set
    Ntotal_array[block] = N * (block + 1)
    #keep track of total number of needles which touched a line
    Ntouches_accumulated += Ntouches_array[block]
    # recalculate pi with on the total number of needles processed thus far
    pi_approximation_array[block] = approximate_pi(Ntotal_array[block], Ntouches_accumulated, L, D)
    
# text output
cw = 18
print(f"{"needles touching":>{cw}}\t{"total needles":>{cw}}\t{"approximation pi":>{cw}}")
for ntouch, ntotal, pi in zip(Ntouches_array, Ntotal_array, pi_approximation_array):
    print(f"{ntouch:>{cw}}\t{ntotal:>{cw}}\t{pi:>{cw}.8f}")
    
    
# ***********  plotting using matplotlib  ***********

# gridspec object defines subplots and their relative size

gs1 = GridSpec(1, 2, width_ratios=[1, 2], height_ratios=[1])
gs2 = GridSpec(2, 2, width_ratios=[1, 2], height_ratios=[1, 1])

runs_array = np.arange(1, Nruns+1) # used for x axis in plots

# create new figure object
fig = plt.figure(figsize = (15, 10), num = "Buffon's needle", facecolor = color_background)

# overal title
title = f"""Approximation of PI using \"Buffon's needle\" in Python
Using {Nruns} sets of {N} needles"""
plt.suptitle(title, fontweight = "bold", size = text_size + 4)

# subplot for image
ax = fig.add_subplot(gs1[0])
ax.set_facecolor(color_plot_background)
ax.set_xticks([])
ax.set_yticks([])
img = Image.open("buffons_needle.png")
ax.imshow(img)

# subplot with bar diagram
ax = fig.add_subplot(gs2[1])
ax.set_title(f"Number of needles touching a line in each set", fontweight = "bold", size = text_size, y = 1.01)
ax.set_facecolor(color_plot_background)
ax.set_xlim(0,Nruns+1)
ax.bar(runs_array, Ntouches_array, 
    label = "Number of needles touching a line", color = colors_plot[0])
ax.bar(runs_array, N - Ntouches_array, bottom = Ntouches_array, 
    label = "Number of needles NOT touching a line", color = colors_plot[1])
ax.legend(fontsize = text_size)
ax.tick_params(labelsize = text_size)
ax.grid(visible = True)

# subplot with line diagram
ax = fig.add_subplot(gs2[3])
ax.set_title(f"Approximation of PI after each set of random needles", fontweight = "bold", size = text_size, y = 1.01)
ax.set_facecolor(color_plot_background)
deviation = np.max(abs(pi_approximation_array - np.pi)) * 1.1
ax.set_ylim(np.pi - deviation, np.pi + deviation)
ax.set_xlim(0,Nruns+1)
ax.fill_between(runs_array, pi_approximation_array, y2 = np.pi, 
    alpha = 0.3, color = colors_plot[2], label = "Deviation from actual value")
ax.plot(runs_array, pi_approximation_array, linewidth = 2, 
    linestyle = "-",
    marker = "o",
    label = "Approximation of PI",
    color = colors_plot[0])
ax.axhline(y = np.pi, color = colors_plot[1], linewidth = 2, label = "Actual value of PI")
ax.legend(fontsize = text_size)
ax.tick_params(labelsize = text_size)
ax.grid(visible = True)

# define space between subplots
plt.subplots_adjust(wspace = 0.11, hspace = 0.28, left = 0.02, right = 0.98, bottom = 0.04, top = 0.857)

# start with plot window maximized, this works at least in linux..
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

plt.show()    


