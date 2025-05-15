# Julia set
# This code calculates a image of the Julia set, it uses numpy for vectorized calculations and
# matplotlib for display. The image can be saved as png image file
# this code is shared without any warranty or implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE
#
# This version has parameters set to view the complete julia fractal

import numpy as np
import matplotlib.pyplot as plt

# Parameters for calculation
image_width = 1200
image_height = 900
# complete image
x_low, x_high = -1.5, 1.5
y_low, y_high = -1.0, 1.0
# these coordinates provide a zoomed in view
#x_low, x_high = -0.1, 0.0999
#y_low, y_high = -0.0833, 0.0833
#x_low, x_high = 0.38, 0.85
#y_low, y_high = -0.02, 0.333
number_iterations = 700 
z_threshold = 2.0
c_initial = -0.512511498387847167 + 0.521295573094847167j # very sensitive
# Parameters for viewing
color_background = "#202020"
vmax_imshow = 400 # upper limit of range on which colormap is applied
color_map = "inferno" # other examples: "magma" "inferno" "hot" "CMRmap" "nipy_spectral"
png_filename = "julia.png"
text_size = 14

print("julia Set using Python, numpy and matplotlib")
print("--------------------------------------------")

# prepare numpy arrays for all values of c, z and the julia_array image
x = np.linspace(x_low, x_high, image_width)
y = np.linspace(y_low, y_high, image_height)
xx, yy = np.meshgrid(x, y)
# the array with all complex values for z
z_array = xx + 1j*yy
# the array with the initial values for c
c_array = np.full(z_array.shape, c_initial)
# the array which will be filled to cantain the julia_array image
julia_array = np.zeros(c_array.shape, dtype = np.uint8)
# this array contains boolean variables to store which z values exceed the threshold
z_exceed_threshold_array = np.full(c_array.shape, False)
print(f"Starting {number_iterations} iterations of {julia_array.shape} array")
# the loop calculates z values for the complete array in each iteration
for counter in range(number_iterations):
    # calculate the next z values for those elements which do not (yet) exceed threshold
    z_array = np.where(z_exceed_threshold_array == False, z_array ** 2 + c_array, z_array)
    # decide which elements of the new z values exceed threshold
    z_exceed_threshold_array = np.abs(z_array) >= z_threshold
    # update julia_array with counter value for those elemenst which exceed threshold for the first time
    julia_array = np.where(julia_array == 0, z_exceed_threshold_array * counter, julia_array)
    if counter % 10 == 0:
        print(f"Iteration {counter} of {number_iterations} completed\r", end = "")

# optionally save the julia array as an png image file
print(f"julia image of {julia_array.shape} created")
answer = input(f"Save as \"{png_filename}\" image file? y/n ").lower()
if answer == "y":
    plt.imsave(png_filename,
        julia_array, 
        cmap = color_map, 
        origin='lower',
        vmin = 0,
        vmax = vmax_imshow)
    print(f"Saved as \"{png_filename}\"")

# create data for axis labels
x_label_pos = np.linspace(0, image_width, 10)
x_label = [f"{x:.5f}" for x in np.linspace(x_low, x_high, 10)]
y_label_pos = np.linspace(0, image_height, 10)
y_label = [f"{y:.5f}" for y in np.linspace(y_low, y_high, 10)]

# display julia array in a matplotlib window, create new figure object
fig = plt.figure(figsize = (15, 10), num = "Julia", facecolor = color_background)
# use dark style wth white letters and set title
plt.style.use('dark_background')
plt.title("julia", 
            fontsize = text_size + 2, fontweight = "bold", y = 1.02)
# set labels on axes
plt.xticks(ticks = x_label_pos, labels = x_label)
plt.yticks(ticks = y_label_pos, labels = y_label)
plt.tick_params(labelsize = text_size)
# display the julia array as an image
plt.imshow(julia_array, 
    cmap = color_map, 
    origin='lower',
    vmin = 0,
    vmax = vmax_imshow)
# define space between image and borders
plt.subplots_adjust(left = 0.08, right = 0.95, bottom = 0.05, top = 0.915)

plt.show()
