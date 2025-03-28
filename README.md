# small-Python-projects
small pieces of Python code

## decimal_degrees_to_dms.py
Contains one function that takes an angle as float and returns degrees, minutes, seconds as tuple
A second function takes tuple of  degrees, minutes, seconds and returns string representation   

## pasword_generator _v2.py
generate a password of given length containing numbers, upper case letters,
lower case letters and optionally symbols

## function_sortandfilter_v2.py
function which accepts a list of strings, removes duplicates, sorts alphabetically
and fiters using a optional search string

## class_color_code.py
contains three class definitions:

### class resistor()
contains code to find the value of a resistor 
out of the color codes present on the component
can return a tuple containing (value, tolerance) as values
or a string representation such as "12 MOhm 5%"

### class resistance()
contains code to find the colorband colors
out of the value and tolerance of the component
both for sets of 4 and 5 colorbands 

### class colors
contains dictionaries to facilitate printing in
color in the console using ANSI escape sequences

## get_color_codes.py
find the color code of a resistor using the classes in class_color_code.py
prints the color bands in color on a console using ANSI escape sequences.

## get_value_from_color_codes.py
find the value and tolerance of a resistor based on the color bands.
It uses the classes in class_color_code.py and prints color bands in color
using ANSI escape sequences.

## logistic_map_test_v2.py
![logistic_map_test_v2.jpg](logistic_map_test_v2.jpg)
Generating a bifurcation diagram of the Logistic Map.
using Numpy and Matplotlib

## recursive_tree_canvas_v4.py
![recursive_tree_canvas_v4.png](recursive_tree_canvas_v4.png)
 Drawing recursive trees on a Tkinter canvas. Four different looking
 trees are drawn using the same code with different parameters.
 Function branch() draws one branch and calls function start_new_branches().
 Function start_new_branches() calls branch() three times to draw branches
 with different angles. Recursion depth is controlled by parameter number_of_recursions
