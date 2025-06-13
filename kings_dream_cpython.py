import matplotlib.pyplot as plt
import numpy as np
from math import *

# parameters for calculation
image_width=2000
image_height=1500
number_iterations = 8000000
# constants for fractal
a = 2.879879 
b = -0.765145
c = -0.966918
d = 0.744728
# Parameters for viewing
color_background = "#202020"
color_map = "inferno" # other examples: "magma" "inferno" "hot" "CMRmap" "nipy_spectral"
png_filename = "kingsdream.png"
text_size = 14

def calc_fractal(N):
    print(f"Calculating fractal\n{N} iterations\n{image_height} rows, {image_width} colums")
    fractal=np.zeros((image_height,image_width))
    x,y=2.0,2.0 # initial values
    step_feedback = N // 10  # only for printing progress
    for counter in range(N):
        x,y = sin(a*x)+b*sin(a*y), sin(c*x)+d*sin(c*y)
#       x,y = sin(a*x)+b*sin(a*y*1.3), sin(c*x)+d*sin(c*y*2)
#       x,y = sin(a*x*1.2)+b*sin(a*y*0.9), sin(c*x*1.4)+d*sin(c*y*2)
        column = int(image_width * (x + 2) / 4)
        row = int(image_height *(y + 2) / 4)
        fractal[row,column] += 1
        if counter % step_feedback == 0:
            print(f"Iteration {counter} of {number_iterations} completed")
    return fractal

def log_convert(fractal):
    # apply a log conversion for showing and saving fractal
    # matplotlib.pyplot.imsave() does not seem to support norm="log" option as imshow() does
    fractal[fractal==0.] = np.nan # avoid log(0) warnings, replace 0.0 with nan
    fractal = np.log(fractal)
    fractal[np.isnan(fractal)] = 0. # imsave does not like the nan values, replace nan back with zeros
    return(fractal)

def save_image(fractal, fname):
    # optionally save the mandelbrot array as an png image file
    print(f"Fractal image of {fractal.shape} created")
    answer = input(f"Save as \"{fname}\" image file? y/n ").lower()
    if answer == "y":
        plt.imsave(fname,
            fractal, 
            cmap = color_map, 
            origin='lower')
        print(f"Saved as \"{fname}\"")

def plot_fractal(fractal):
    # display fractal on matplotlib window
    fig = plt.figure(figsize = (15, 10), num = "King's Dream Fractal", facecolor = color_background)
    plt.style.use('dark_background')
    plt.title("King's Dream Fractal", 
                fontsize = text_size + 2, fontweight = "bold", y = 1.02)
    plt.imshow(fractal, 
        cmap = color_map, 
        origin='lower')
    plt.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.05, top = 0.915)
    plt.show()

# calculate fractal
pixel_array = calc_fractal(number_iterations)
# log convertion to make smaller values more visible
pixel_array = log_convert(pixel_array)
# optionally save as png image file
save_image(pixel_array, png_filename)
# display fractal
plot_fractal(pixel_array)
