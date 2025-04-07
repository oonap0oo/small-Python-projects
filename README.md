# small-Python-projects
small pieces of Python code

## sierpinski_triangle_tkinter_v6.py
![sierpinski_triangle_tkinter_v6_screenshot.png](sierpinski_triangle_tkinter_v6_screenshot.png)
Sierpinski Triangle constructed using the Chaos game method. 
It rotates and scales in and out.
The triangle is drawn on a tkinter canvas widget.

## pascal_triangle_ansi.py
![pascal_triangle.png](pascal_triangle.png)
This code calculates the first 32 rows of Pascal's triangle.
It then prints the last digit of each value
by marking if that digit is uneven, the Sierpinski triangle appears.
This version uses ANSI escape codes to generate colors and reverse characters

## pascal_triangle_no_ansi_v2.py
This code calculates the first 32 rows of Pascal's triangle
It then prints the last digit of each value
by marking if that digit is uneven, the Sierpinski triangle appears.
This version avoids using ANSI escape codes by reprinting the triangle
using a character in place of uneven values

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

## pi_monte_carlo_circle.py
 ![pi_monte_carlo_circle_plots.png](pi_monte_carlo_circle_plots.png)
Monte Carlo approximation of PI, using Python and Numpy. 
A series of points with random x,y coördinates are calculated, whether they fall inside the unit circle can be used to approximate the value of PI. Calculations are done in a series of parts called intervals. The code keeps track of the successive PI approximations taking the extra data into account after each interval, it prints a table and plots a graph. 

## perimeter_ellipse_v4.py
![perimeter_ellipse_v4_py.png](perimeter_ellipse_v4_py.png)
Three methods to approximate the Circumference of an ellipse, using Python + Scipy + Numpy + Matplotlib
The Circumference of a series of elipses with identical surface area is calculated,
the shape ranging from a circle to the flattest ellipse.
Using the complete elliptic integral of the second kind function ellipe() and
the Binomial coefficients function binom() from scipy.special.

## wbridge.py
Calculate output voltage of a Wheatstone Bridge as function of one
variable resistor Rx using Kirchhoff circuit laws and left division operator with a matrix and vector.
Made to compare code with a GNU Octave script doing the same calculations: [wbridge.m](https://github.com/oonap0oo/GNU_Octave_scripts/blob/23891978e31cf807bc051fc30719fc4f2e71cebe/wbridge.m)


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

## several_methods_fibonacci_sequence_v2.py
These 6 different Python functions generate the same list containing a specified number of Fibonacci numbers.
Included are a generator function, recursive functions with and without memoization, 
a function from the sympy library and Binet's formula, a closed-form expression.


