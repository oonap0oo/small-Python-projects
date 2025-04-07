#!/usr/bin/env python3
#
#  pascal_triangle_ansi.py
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
#  This code claculates the first 32 rows of Pascal's triangle
#  It then prints the last digit of each value
#  by marking if that digit is uneven, the Sierpinski triangle appears

# ansi commands "reverse" + "brightyellow foreground color" + "black background color"
ansi_mark = "\033[07m\033[93m\033[40m"
# ansi command to reset
ansi_reset = "\033[0m"

offset = " " * 4

# function returns True if value is an even number
def iseven(value):
    return((value % 2) == 0)

# initialise the pascal triangle and fill in the first row
# variable pascal_triangle will be a list of lists
# each sublist represents a row in the triangle
pascal_triangle = [[1]]

# generate the following rows of the triangle
for row in range(1, 32):
    # initialise the list for a new row
    new_row = [1]
    # fill the new row with the sums of the two values situated above in the triangle
    for column in range(1, row):
        new_row.append(pascal_triangle[row - 1][column - 1] + pascal_triangle[row - 1][column])
    # add the 1 at the end of each row
    new_row.append(1)
    # add the new row to the triangle
    pascal_triangle.append(new_row)

# title for output  
title = f"""
        Pascal's triangle showing the last digit of each number
        Marking the {ansi_mark}uneven digits{ansi_reset} shows a Sierpinski triangle
"""  
print(title)

# iterate through the triangle, use enumerate to get row number
# as well as a list of the row values
for row_number, row_as_list in enumerate(pascal_triangle):
    #initialise an empty string which will be usd to print a row
    row_as_str = ""
    # iterate through the row 
    for value in row_as_list:
        # determine the last digit
        last_digit = value % 10
        # if the last digit is uneven, it will be printed reverse and colored
        if iseven(last_digit):
            row_as_str += f"{last_digit} "
        else:
            row_as_str += f"{ansi_mark}{last_digit}{ansi_reset} "
    # print the string representation of the row with added spaces to
    # get the triangle shape
    print(offset + " " * (31 - row_number) + row_as_str)


        


