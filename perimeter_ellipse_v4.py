#!/usr/bin/env python3
#
#  perimeter_ellipse_v4.py
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
#  
#  Three methods to approximate the Circumference of an ellipse, using Python + Scipy + Numpy + Matplotlib
#  the Circumference of a series of elipses with identical surface area is calculated 
#  the shape ranging from a circle to the flattest ellipse
#  importing the complete elliptic integral of the second kind function ellipe() and
#  the Binomial coefficients function binom() from scipy.special
#
from scipy.special import ellipe, binom
# importing library numpy to be able to define calculations on complete vectors of numbers (np arrays)
import numpy as np
# importing matplotlib.pyplot, it contains basic plotting functionality
import matplotlib.pyplot as plt
# importing matplotlib.patches to be able to draw ellipses directly on the plot window
from matplotlib.patches import Ellipse
# importing matplotlib.colors to use predefined colors
import matplotlib.colors as mcolors


title = "Three methods to approximate the Circumference of an ellipse, using Python + Scipy, Numpy"
info = """
Ellipse:
--------

        x²/a² + y²/b² = 1

Method 1, Elliptic integral:
----------------------------

        e is the eccentricity of the ellipse:
        
        e = √( 1 - b² / a² ), a > b
        
                            π/2 
        Circumference = 4.a.∫ √( 1 - e².sin²(θ) ).d(θ)
                            0
        
        complete elliptic integral of the second kind:
                π/2 
        E(x) =  ∫ √( 1 - x.sin(θ) ).d(θ)
                0
        
        Circumference = 4.a.E( e² )
        
        Calculated using scipy.special.ellipe() for the complete elliptic integral of the second kind

Method 2, Simple Arithmetic-Geometric Mean approximation:
---------------------------------------------------------

        Circumference ≈ √(2).π.√( a² + b² )

Method 3, Circumference approximation by series:
------------------------------------------------

        h = (a - b)² / (a + b)²
                                  ∞
        Circumference = π.(a + b).∑ ( binom(2.n, n) / ((2.n - 1) * 4ⁿ ) )²
                                 n=0
 
        Circumference = π.(a + b).( 1 + h / 4 + h²/64 + h³/256 + 25.h⁴/16384 + 49.h⁵/65536 + ... )
        
        Calculated using using scipy.special.binom() for the Binomial coefficient
    
"""
print(title)
print("-" * len(title))
print(info)



# Complete elliptic integral of the second kind:
#   e is the eccentricity of the ellipse:
#   e = √( 1 - b² / a² ) 
#   a >= b
#               π/2 
#       E(x) =  ∫ √( 1 - x.sin(θ) ).d(θ)
#               0
#        
#       Circumference = 4.a.E( e² )
#
#       calculated using scipy.integrate.quad()
#
def Circumference_by_Elliptic_integral(a , b):
    half_pi = np.pi / 2.0
    # eccentricity of the ellipse
    e_sq = 1 - b ** 2 / a ** 2
    e = np.sqrt(e_sq)
    # call scipy function to perform integration
    integral = ellipe(e_sq)
    Circumference = 4 * a * integral
    return(Circumference, e)


# Simple arithmetic-geometric mean approximation
#   Circumference ≈ 2.π.√( ( a² + b² ) / 2 )
#                 = √(2).π.√( a² + b² )
#    
def Circumference_by_Simple_Arithmetic_Geometric_Mean_Approximation(a, b):
    Circumference = np.sqrt(2) * np.pi * np.sqrt( a ** 2 + b ** 2)
    return(Circumference)
    

# Circumference approximation by series
#       h = (a - b)² / (a + b)²
#                                 ∞
#       Circumference = π.(a + b).∑ ( binom(2.n, n) / ((2.n - 1) * 4ⁿ ) )²
#                                n=0
#       Circumference = π.(a + b).( 1 + h / 4 + h²/64 + h³/256 + 25.h⁴/16384 + 49.h⁵/65536 + ... )
#
#       Using scipy.special.binom() for the Binomial coefficient
#
def Circumference_by_Series_Approximation(a, b, number_of_terms):
    h = (a - b) ** 2 / (a + b) ** 2
    series = 0
    # calculate coefficients and add the terms of the series
    for n in range(number_of_terms):
        coefficient = ( binom( 2 * n, n) / ((2 * n - 1) * 4 ** n) ) ** 2
        series += coefficient * h ** n
    Circumference = series * np.pi * (a + b)
    return(Circumference)



# varying a en b values so that the surface area of the
# ellipse stays constant
# area = pi.a.b
# also a >= b for the elliptic integral method
# here pi is chosen as area, so as in circle with a=1 and b=1

# number of ellipses
N = 15

# maximum value of a, minimum will be 1
a_max = 8

# number of terms for the series approximation
number_of_terms = 6

# values for a
array_a = np.linspace(1, a_max, N)

# values for b so that area stays constant
array_b = 1.0 / array_a

# as a check calculate area for each a and b pair
array_area = np.pi * array_a * array_b

# these approximations can be calculated array based using numpy
Circumference_elliptic, eccentricity = Circumference_by_Elliptic_integral(array_a, array_b)
Circumference_geometric = Circumference_by_Simple_Arithmetic_Geometric_Mean_Approximation(array_a, array_b)
Circumference_series = Circumference_by_Series_Approximation(array_a, array_b, number_of_terms)

# calculate percentage difference of Series method vs Ellliptic
percentage_delta_elliptic_series = 100.0 * ( Circumference_elliptic - Circumference_series ) / Circumference_elliptic


# print table of all results
print(f"Calculating circumference of {N} ellipses, with a ranging from 1 to {a_max} and b from 1 to {1 / a_max}\n")
header = "|\t".join(["     a","     b","Eccentricity","        Area","     Geometric",f"Series {number_of_terms} terms","      Elliptic"])
print(header)
print("-" * 94)
for index, a, b, area in zip(range(N), array_a, array_b, array_area):
    table_line = f"{a:>6.3f}|\t{b:>6.3f}|\t{eccentricity[index]:>12.8f}|\t{area:>12.8f}|\t"
    table_line += f"{Circumference_geometric[index]:>14.8f}|\t{Circumference_series[index]:>14.8f}|\t{Circumference_elliptic[index]:>14.8f}"
    print(table_line)

    
# make plots
# a numpy array which contains a subset of the values in array_a, it determines where to plot x axis labels
x_axis_a_ticks = array_a[::2]
# a list which contains the x axis labels as strings
x_axis_a_labels = [ f"{a:.1f},\n{b:.3f}" for a,b in zip(array_a[::2], array_b[::2]) ]

# a new patplotlib figure object is created to start defining the plot window
plt.figure(figsize=(15, 10), num = title)

# sub plot to show the shapes of the ellipses
plt.subplot(2, 1, 1)
ax = plt.gca()
colors = tuple(mcolors.TABLEAU_COLORS.values())
for index, a, b in zip(range(N), array_a, array_b):
    ellipse = Ellipse(xy = (0, 0), width = 2*a, height = 2*b, edgecolor = colors[index % len(colors)], fc = "None", lw = 2)
    ax.add_patch(ellipse)
plt.axis('equal')
plt.grid()
txt = f"x²/a² + y²/b² = 1\n a = 1 .. {a_max}\n b = 1 .. {1 / a_max}"
plt.text(-a_max, 0.5, txt, fontsize = "xx-large", fontfamily = "monospace", backgroundcolor = "w")
plt.title(f"Shapes of the {N} ellipses calculated, they share the same surface area", fontsize = 18, y = 1.03)

# subplot to show the values of the three methods vs a and b
plt.subplot(2, 2, 3)
plt.plot(array_a, Circumference_elliptic, marker = "x", color = "b", linestyle = "dashed", markersize = 10, label = "Complete Elliptic Integral of the 2nd kind")
plt.plot(array_a, Circumference_geometric, marker = "*", markersize = 10, label = "Simple Arithmetic-geometric mean")
plt.plot(array_a, Circumference_series, marker = "+", color = "r", linestyle = "dotted", markersize = 10, label = f"Approximation by series with {number_of_terms} terms")
plt.legend(fontsize = 15)
plt.title("3 Circumference approximation methods", fontsize = 18, y = 1.03)
plt.xlabel("a,b", fontsize = 15)
plt.ylabel("Circumference approximations", fontsize = 15)
plt.xticks(fontsize = 13)
plt.yticks(fontsize = 13)
ax = plt.gca()
ax.set_xticks(x_axis_a_ticks, labels = x_axis_a_labels)
plt.grid()

# subplot to show how the series approximation differs from Elliptic integral method in %
plt.subplot(2, 2, 4)
plt.plot(array_a, percentage_delta_elliptic_series, marker = "D", label = f"Approximation by series with {number_of_terms} terms\n versus Elliptic integral")
plt.legend(fontsize = 15)
plt.title("% difference, series approx. vs Elliptic integral", fontsize = 18, y = 1.03)
plt.xlabel("a,b", fontsize = 15)
plt.ylabel("% Delta", fontsize = 15)
plt.xticks(fontsize = 13)
plt.yticks(fontsize = 13)
ax = plt.gca()
ax.set_xticks(x_axis_a_ticks, labels = x_axis_a_labels)
plt.grid()

# define space between subplots
plt.tight_layout(pad=3.0)

# start with plot window maximized, this works at least in linux..
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

# show window enter the loop
plt.show()


