import matplotlib.pyplot as plt
import numpy as np
from math import *

# parameters for calculation
image_width=1000
image_height=1000
number_iterations = image_width * image_height * 2
midpoint=(0,0)
scale=(15,15)

xrange = (midpoint[0]-scale[0],midpoint[0]+scale[0]); yrange = (midpoint[1]-scale[1],midpoint[1]+scale[1])
# constants for fractal
# "The initial values for x and y can be any floating point value
# between -20 and +20.
# The a parameter can be any floating point value between -1 and +1.
# The b parameter should always stay close to 1. "
a = -0.7
b = 1.0


# Parameters for viewing
color_background = "#202020"
color_map = "nipy_spectral" # other examples: "magma" "inferno" "hot" "CMRmap" "nipy_spectral" 
png_filename = "Gumowski_Mira.png"
text_size = 14

def sign(x):
    return 1 - 2*(x < 0)

def calc_fractal(N,x_range,y_range):
    def expr(x):
        return a * x + 2 * (1 - a) * x**2 / (1 + x**2)**2
    x1, x2 = x_range
    y1, y2 = y_range
    print(f"Calculating fractal\n{N} iterations\n{image_height} rows, {image_width} colums")
    fractal=np.zeros((image_height,image_width))
    x,y=-5.5, -5.0 # initial values
    step_feedback = N // 10  # only for printing progress
    for counter in range(N):
        x_old = x
        x = b*y + expr(x)
        y = expr(x) - x_old
        column = int(image_width * (x - x1) / (x2 - x1))
        row = int(image_height *(y - y1) / (y2 - y1))
        if (row > -1) and (row < image_height) and (column > -1) and (column < image_width):
            fractal[row,column] += 1
        if counter % step_feedback == 0:
            print(f"Iteration {counter} of {number_iterations} completed")
    return fractal

def log_convert(fractal):
    # apply a log conversion for showing and saving fractal
    # matplotlib.pyplot.imsave() does not seem to support norm="log" option as imshow() does.
    print("Applying a log conversion for showing and saving fractal")
    fractal[fractal==0.] = np.nan # avoid log(0) warnings, replace 0.0 with nan
    fractal = np.log(fractal)
    fractal[np.isnan(fractal)] = 0. # imsave does not like the nan values, replace nan back with zeros
    return(fractal)

def save_image(fractal, fname):
    # optionally save the Gumowski-Mira array as an png image file
    print(f"Fractal image of {fractal.shape} created")
    answer = input(f"Save as \"{fname}\" image file? y/n ").lower()
    if answer == "y":
        plt.imsave(fname,
            fractal, 
            cmap = color_map, 
            origin='upper')
        print(f"Saved as \"{fname}\"")

def plot_fractal(fractal):
    # display fractal on matplotlib window
    fig = plt.figure(figsize = (15, 10), num = "Gumowski-Mira Fractal", facecolor = color_background)
    plt.style.use('dark_background')
    plt.title("Gumowski-Mira Fractal", 
                fontsize = text_size + 2, fontweight = "bold", y = 1.02)
    plt.imshow(fractal, 
        cmap = color_map, 
        origin='upper')
    plt.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.05, top = 0.915)
    plt.show()

# calculate fractal
pixel_array = calc_fractal(number_iterations, xrange, yrange)
# log convertion to make smaller values more visible
pixel_array = log_convert(pixel_array)
# optionally save as png image file
save_image(pixel_array, png_filename)
# display fractal
plot_fractal(pixel_array)
