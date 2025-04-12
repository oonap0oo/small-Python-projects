#!/usr/bin/env python3
#
#  logistic_map_calculate_image_v3.py
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
# This code calculates a image of the bifurcation diagram
# for the logistic map 
# Xn+1 = a. Xn.(1 - Xn)
# iterations are done for increasing values of 'a'
# the logistic map is represented as a numpy array
# the image of the map is displayed and can be 
# saved as a PNG image file

# matplotlib is used to display the image
import matplotlib.pyplot as plt
# numpy performs as the calculations
import numpy as np
# PIL is used to save to PNG
from PIL import Image

# *** parameters ****
# total number of iterations
loops = 4000
# Logistic map wil be nrows x ncols array
ncols = 5333
nrows = 3000
# start and end value of parameter a
astart = 3.5
aend = 4.0
# default file name for saving as PNG
filename_default = "logistic.png"

# the numpy array to contain the logistic map is fllled with zeros
# this is the picture to be viewed later, dimensions of logistic 
# are nrows x ncols
logistic = np.zeros((nrows, ncols))

# values for parameter a are defined, a is here a vector of
# increasing values between astart en aend to be 
# used for each column of logistic
a = np.linspace(astart, aend, ncols)

# the initial values for x are defined, x is here a vector holding values to be 
# used for each column of logistic 
x = np.full(ncols, 0.5)

# vector containing all the column indices of logistic map
columns = np.arange(ncols)

print("This code calculates a image of the bifurcation diagram for the logistic map")
print("\n  Xn+1 = a. Xn.(1 - Xn)")
print("\niterations are done for increasing values of 'a'")
print(f"parameter 'a' will range from {astart} to {aend}")
print(f"the logistic map is represented as a {nrows} x {ncols} numpy array")
print("the image of the map is displayed and can be saved as a PNG image file")
print(f"\nstarting {loops} iterations\n") 

# iterate loops and perform calculations for whole array logistic in each step
# through vectorised functionality of numpy
for _ in range(loops):
    # perform logistic function for all x values at once
    # calculate new values for x for all the different a parameters
    # in each loop iteration, both x and a are vectors
    x = a * x * (1.0 - x)  
    # calculate row indices for all values of x it uses a vectorised
    # conversion to integer via .astype(int), 1 is subtracted because
    # index anways starts at zero
    rows = (x * nrows).astype(int) - 1 
    # elements of array logistic are incremented by 1 
    # at rows determined by linear array rows 
    # and over all columns as directed by columns = np.arange(ncols)
    logistic[rows, columns] += 1

# print some info also keep maximum value and average value of array logistic as variables for later
print("Calculations finalised:")
print("  dimensions of array:", logistic.shape)
print("  number of elements:", logistic.size)
print(f"  size of array in MB: {(logistic.nbytes / 1048576):.2f}")
logistic_max = np.max(logistic)
print("  maximum value in array:", logistic_max)
print("  minimum value in array:", np.min(logistic))
logistic_average = np.average(logistic)
print("  average value in array:", logistic_average)


# converting the array logistic to 8 bit integer values between 0 and 255
# loads faster in matplotlib and is suited for saving as image file
# also flipping the image vertically using negative step on the row index
# vmaximum is a clipping value above which pixel greyscale will be 100% white
vmaximum = 7.0 * logistic_average
print("\nConverting the array to 8 bit integer values")
logistic = np.clip(logistic[::-1,:] * 255 / vmaximum, 0, 255).astype(np.uint8)
print(f"size of array in MB: {(logistic.nbytes / 1048576):.2f}")

# save as PNG image file?
answer = input("\nSave PNG file (y/n)? ")

if answer == "y":
    # Define the file name to save the image
    answer = input(f"Name of PNG file?\nhit Enter to save as {filename_default}\n or enter other name:? ")
    if answer == "":
        image_file_name = filename_default # default name if only enter is pressed
    else:
        answer = answer.split(".")[0]
        image_file_name = answer + ".png"
    print(f"saving image as PNG file {image_file_name}")
    
    # Convert the NumPy array to an PIL image object
    image = Image.fromarray(logistic)
    # Use the save method of the image object
    image.save(image_file_name, compress_level = 3)

print("\ngenerating Matplotlib display")

# generate labels for plot axes
nlabels = 8
xloc = np.round(np.linspace(0, ncols, nlabels))
xlabel = np.round(np.linspace(astart, aend, nlabels), decimals=3)
yloc = np.round(np.linspace(0, nrows, nlabels))
ylabel = np.round(np.linspace(1.0, 0.0, nlabels), decimals=3)

# black background and white text, axes
plt.style.use('dark_background')

# generate matplolib figure
plt.figure(figsize = (15, 10), num = f"Logistic map using Python, Numpy and Matplotlib, {np.shape(logistic)}")
# show the values as greyscale image, value determines brightness of pixel
plt.imshow(logistic, cmap='gray')
plt.xticks(xloc, xlabel)
plt.yticks(yloc, ylabel)
plt.gca().set_xlabel('a', fontsize=20)
plt.gca().set_ylabel('x', fontsize=20)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)

# define space between plot and window
plt.subplots_adjust(bottom = 0.06, top = 0.99)

# start with plot window maximized, this works at least in linux..
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

plt.show()
