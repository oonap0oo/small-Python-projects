#!/usr/bin/env python3
#
#  get_color_codes.py
#  
#  Copyright 2025 NaP0
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
# find the color code of a resistor using the classes in class_color_code.py

# import the classes
from class_color_code import *

# generate input
print("Find the resistor color code")
value_answer = input("\nResistor value in Ohm? ")
value = resistance.metricprefixtofloat(value_answer) 
if value is None:
    print(f" {value_answer} is not a valid resistor value, terminating")
    quit()
print("\nTolerance of the resistor in %\nPossible tolerances:")
for possible_tol in resistance.dict_tolerance_to_colors:
    print(f"{possible_tol}%   ", end="")
print()
tol_answer = input("Tolerance? ")
tol = float(tol_answer)

# generate instances of resistance objects for 4 and 5 color bands
try:
    res_4_bands = resistance(value, tol, 4)
    res_5_bands = resistance(value, tol, 5)
except Exception as e:
    print(e)
    quit()

# generate output
print(f"\nResistor of {value} Ohm with tolerance of {tol}%\n")

# 4 color bands
print("color bands for 4 band resistors :",res_4_bands)
print("Looks like this:")
for band in res_4_bands.ansistringscolorbands():
    print(band)

# 5 color bands    
print("\ncolor bands for 5 band resistors :",res_5_bands)
print("Looks like this:")
for band in res_5_bands.ansistringscolorbands():
    print(band)
