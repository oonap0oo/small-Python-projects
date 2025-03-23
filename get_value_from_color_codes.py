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
# find the value and tolerance of a resistor from given color codes
# using the classes in class_color_code.py

# import the classes
from class_color_code import *

# a function to get a valid integer as user input with checks 
def num_input_check(valid_answers, prompt = ""):
    valid = False
    while not valid:
        answer = input(prompt)
        if answer.isnumeric():
            int_answer = int( answer )
            if int_answer in valid_answers:
                valid = True
            else:
                print(f"{answer} not within {valid_answers}")
        else:
            print("invalid input:", answer)
    return(int_answer)

# a function to get a valid string as user input with checks 
def str_input_check(valid_answers, prompt = ""):
    valid = False
    while not valid:
        answer = input(prompt).lower().strip()
        if answer in valid_answers:
            valid = True
        else:
            print(f"{answer} not one of possible choices: {tuple(valid_answers)}")
    return(answer)
    
# words to be used 
digit_names = ("first","second","third","fourth","fifth")  
# the list to contain the given color names
color_bands = []    

# title
print("Get resistor value from the color code")
print("--------------------------------------")

# get number of color bands, valid number of bands is 4 or 5
number_bands = num_input_check((4,5), "Number of color bands, 4 or 5 ? ")

# the number of digit color bands depends on total number of bands
number_of_digits = number_bands - 2

# get digit color bands

# show possible colors
print(f"\nFirst the {number_of_digits} color bands for the digits")
print("Here are the possible colors:")
for name in resistor.dict_colors.keys():
    ansi = colors.dict_set_resistor_colors_for_print[name]
    color = colors.commands["bold"] + ansi + name.center(8) + colors.commands["reset"] + " "
    print(color * number_of_digits)

# get input of digit color bands
for digit in range(number_of_digits):
    color_name = str_input_check(resistor.dict_colors.keys(), 
        f"\nGive the name of the {digit_names[ digit ]} color band? ")
    print(f"{color_name} selected for {digit_names[ digit ]} color band")
    color_bands.append(color_name)

# get multiplier color bands

# show possible colors
digit = number_bands - 2
print(f"\nNow the {digit_names[ digit ]} color band for the multiplier")
print("Here are the possible colors:")
for name in resistor.dict_multiplier_colors.keys():
    ansi = colors.dict_set_resistor_colors_for_print[name]
    color = colors.commands["bold"] + ansi + name.center(8) + colors.commands["reset"] + " "
    print(color)
    
# get input of multiplier color bands
color_name = str_input_check(resistor.dict_multiplier_colors.keys(), 
    f"\nGive the name of the {digit_names[ digit ]} color band? ")
print(f"{color_name} selected for {digit_names[ digit ]} color band")
color_bands.append(color_name)

# get tolerance color bands

# show possible colors
digit = number_bands - 1
print(f"\nNow the {digit_names[ digit ]} color band for the tolerance")
print("Here are the possible colors:")
for name in resistor.dict_tolerance_colors.keys():
    ansi = colors.dict_set_resistor_colors_for_print[name]
    color = colors.commands["bold"] + ansi + name.center(8) + colors.commands["reset"] + " "
    print(color)
    
# get input of tolerance color bands
color_name = str_input_check(resistor.dict_tolerance_colors.keys(), 
    f"\nGive the name of the {digit_names[ digit ]} color band? ")
print(f"{color_name} selected for {digit_names[ digit ]} color band")
color_bands.append(color_name)

# summarise the given colors
print(f"\nThe resistor has following {number_bands} color bands:")
for name in color_bands:
    ansi = colors.dict_set_resistor_colors_for_print[name]
    color = colors.commands["bold"] + ansi + name.center(8) + colors.commands["reset"] + " "
    print(color)
    
# create instance of resistor with the color bands as argument
resistor_instance = resistor(color_bands)

# output value and tolerance
print(colors.commands["bold"], end="")
print(f"\nThe resistor has value of {colors.commands['reverse']}{str(resistor_instance)}")
print(colors.commands["reset"], end="")

