# MONTE CARLO ANALYSIS USING PYTHON, NUMPY AND MATPLOTLIB
# this code performs a Monte Carlo analysis of a voltage divider with two resistors
# Numpy is used to generate the random values with a normal distribution
# matplotlib is used to generate the plot
# this code is shared without any warranty or implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec # align subplots also with variable size


 # ****  PARAMETERS  ****
Vin = 5.0
r1_nominal = 1e3 # upper resistor
r2_nominal = 1e3 # lower resistor
tolerance = 0.01 # of both resistors
ratio_tol_stddev = 3.0 # ratio of tolerance / standard deviation
number_of_samples = 10000
number_of_bins = 30
# plots
text_size = 15
color_plot_background = "#F0F0F0"
color_background = "#E0E0E0"
color_table_header = "#C0C0C0"

# generate arrays of resistor values for r1 and r2 with normal distribution
rng = np.random.default_rng() # a numpy random generator object
r1_array = rng.normal(r1_nominal, r1_nominal * tolerance / ratio_tol_stddev, number_of_samples)
r2_array = rng.normal(r2_nominal, r2_nominal * tolerance / ratio_tol_stddev, number_of_samples)
# clip the values so that none exceed the tolerance specification
r1_array = np.clip(r1_array, r1_nominal * (1 - tolerance), r1_nominal * (1 + tolerance))
r2_array = np.clip(r2_array, r2_nominal * (1 - tolerance), r2_nominal * (1 + tolerance))

# define the voltage divider output voltage
def voltage_divider(r_upper, r_lower, v_input):
    return( v_input * r_lower / (r_lower + r_upper) )

# calculate the array of output voltages
v_output = voltage_divider(r1_array, r2_array, Vin)

# statistics of output voltage
v_output_average = np.mean(v_output)


# gridspec object defines subplots and their relative size
gs = GridSpec(2, 2, width_ratios=[2, 3], height_ratios=[1, 1])

# plotting

fig = plt.figure(figsize = (15, 10), num = 1, facecolor = color_background)

# overal title
plt.suptitle(f"Monte Carlo analysis of voltage divider", 
            fontweight = "bold", size = text_size + 3)

# subplot showing histogram of r1
plt.subplot(gs[0])
plt.title("Values of resistor r1", 
            fontsize = text_size + 2, fontweight = "bold", y = 1.02)
plt.xlabel("resistance [Ohm]", fontsize = text_size)
plt.ylabel("quantities", fontsize = text_size)
plt.tick_params(labelsize = text_size - 1)
plt.gca().set_facecolor(color_plot_background) 
plt.grid(visible = True)
plt.hist(r1_array, number_of_bins, label = f"{r1_nominal} +- {tolerance * 100}%")
plt.legend(fontsize = text_size)


# subplot showing histogram of r2
plt.subplot(gs[2])
plt.title("Values of resistors r1", 
            fontsize = text_size + 2, fontweight = "bold", y = 1.02)
plt.xlabel("resistance [Ohm]", fontsize = text_size)
plt.ylabel("quantities", fontsize = text_size)
plt.tick_params(labelsize = text_size - 1)
plt.gca().set_facecolor(color_plot_background) 
plt.grid(visible = True)
plt.hist(r2_array, number_of_bins, label = f"{r2_nominal} +- {tolerance * 100}%")
plt.legend(fontsize = text_size)


# subplot showing table
plt.subplot(gs[1])
plt.title(f"Statistics after {number_of_samples} runs", 
            fontsize = text_size + 2, fontweight = "bold", y = 1.02)
plt.gca().set_facecolor(color_plot_background) 
plt.axis(False)
table_col_labels = ["", "Nominal", "Average",  "3 x Std Dev", "Max", "Min"]
table_data = [
["Vin",f"{Vin} V","-","-","-","-"],
["r1, upper res.", f"{r1_nominal} Ohm", f"{np.mean(r1_array):.1f} Ohm", f"{3 * np.std(r1_array):.1f} Ohm", f"{np.max(r1_array):.1f} Ohm", f"{np.min(r1_array):.1f} Ohm"],
["r2, lower res.", f"{r2_nominal} Ohm", f"{np.mean(r2_array):.1f} Ohm", f"{3 * np.std(r2_array):.1f} Ohm", f"{np.max(r2_array):.1f} Ohm", f"{np.min(r2_array):.1f} Ohm"],
["Vout", f"{voltage_divider(r1_nominal, r2_nominal, Vin):.3f} V", f"{np.mean(v_output):.3f} V", f"{3 * np.std(v_output):.3f} V", f"{np.max(v_output):.3f} V", f"{np.min(v_output):.3f} V"]
]
table_object = plt.table(table_data, colLabels = table_col_labels, 
        cellColours = [[color_plot_background] * 6] * 4, loc = "center", cellLoc = "center",
        colColours = [color_table_header] * 6)
table_object.auto_set_font_size(False)
table_object.set_fontsize(text_size - 1)
table_object.scale(1, 4)


# subplot showing histogram of Vout
plt.subplot(gs[3])
plt.title(f"Output voltage for input voltage of {Vin} V", 
            fontsize = text_size + 2, fontweight = "bold", y = 1.02)
plt.xlabel("voltage [V]", fontsize = text_size)
plt.ylabel("quantities", fontsize = text_size)
plt.tick_params(labelsize = text_size)
plt.gca().set_facecolor(color_plot_background) 
plt.grid(visible = True)
plt.hist(v_output, number_of_bins, label = f"Average {v_output_average:.3f}V")
plt.legend(fontsize = text_size)


# define space between subplots
plt.subplots_adjust(wspace = 0.16, hspace = 0.38, left = 0.06, right = 0.97, bottom = 0.07, top = 0.87)

# start with plot window maximized, this works at least in linux..
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

plt.show()
