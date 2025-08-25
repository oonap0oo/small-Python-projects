# Spirograph

# R: radius larger outer wheel
# tau: radius smaller inner wheel
# rho : distance pen from center of small wheel
# t: polar coordinate is angle over which inner wheel
#    has travelled inside outer wheel
# t2: equivalent of t but for coordinate system
#     which has origin in center of smaller wheel
# x: x coordinate of pen position
# y: y coordinate of pen position

# x = (R - tau) * cos(t) + rho * cos( tau * t2 )
# y = (R - tau) * sin(t) + rho * sin( tau * t2 )

# t * R = t * tau + (-t2) * tau
# => t2 = -t * (R - tau) / tau

# x = (R - tau) * cos(t) + rho * cos( (R - tau) / tau * t )
# y = (R - tau) * sin(t) - rho * sin( (R - tau) / tau * t )

# starting the drawing with an offset angle, tilts the figure

# x = (R - tau) * cos(t + offset) + rho * cos( (R - tau) / tau * t )
# y = (R - tau) * sin(t + offset) - rho * sin( (R - tau) / tau * t )

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

# returns x,y coordinates of pen on the spirograph
def calc_xy(t):
    x = (R - tau) * np.cos(t + offset) + rho * np.cos( (R - tau) / tau * t )
    y = (R - tau) * np.sin(t + offset) - rho * np.sin( (R - tau) / tau * t )
    return(x,y)


# parameters
# R: radius outer wheel is also related to number of teeth
R = 144
#tau: radius smaller inner wheel is also related to number of teeth
tau = 84  #102 #63 
# range of rho values (min, max)
range_rho = (tau * 0.05, tau * 0.95)
# maximum offset
max_offset = np.pi / 3
# number of combinations: offset + rho
number_of_combinations = 16

# determine number of turns
number_of_turns = np.lcm(R, tau) // R
print(f"Number of turns around outer big wheel: {number_of_turns}")
print(f"Number of turns of inner small wheel: {np.lcm(R, tau) // tau}")

# maximum value parameter angle t is number of turns times 2.pi
max_t = number_of_turns * 2 * np.pi

# plot parameters
color_plot_background = "black"
colors = list(matplotlib.colors.TABLEAU_COLORS)
number_points = 100 * number_of_turns

# prepare array with t values
t_arr = np.linspace(0, max_t, number_points)

# plot window
plt.figure(num = f"Spirograph outer={R}, inner={tau}, {number_of_combinations} combinations ",
           figsize = (10, 10),
           layout = "compressed"
           )

plt.axis("equal")
plt.gca().set_facecolor(color_plot_background)

# remove ticks
plt.xticks([])
plt.yticks([])

# rho: distance position drawing pen from center of smaller wheel
rho_values = np.linspace(range_rho[0], range_rho[1], number_of_combinations)

# offset: inner wheel starts at increasing offset angle for each set of turns
offset_values = np.linspace(0, max_offset, number_of_combinations)

# numbering of the plots, prepare as np array
plot_number_values = np.arange(number_of_combinations)

for plot_number, rho, offset in zip(plot_number_values, rho_values, offset_values):
    x_arr, y_arr = calc_xy(t_arr)
    color_number = plot_number % len(colors)
    plt.plot(x_arr ,y_arr ,linewidth = 2, color = colors[color_number])

plt.show()
