#!/usr/bin/env python3
#
#  several_methods_fibonacci_sequence_v2.py
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
# Several different functions which return a list containing the first 20
# values of the Fibonacci sequence
# 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...

print("Several different functions which return a list containing")
print("the first 20 values of the Fibonacci sequence")

# ---------------------------------------------------------------------
# function 1 : simple for-loop which returns a list
# ---------------------------------------------------------------------
def Fibonacci_1( number_of_values: int) -> list:
    list_fib = [ 0, 1 ]
    for index in range(2,number_of_values):
        new_value = list_fib[index - 1] + list_fib[index - 2]
        list_fib.append(new_value)
    return(list_fib)

print("\nFunction 1: simple for-loop")
print(Fibonacci_1(20))
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# function 2 : using a generator function with for loop which 
# yields each value. the generator is converted to a list
# ---------------------------------------------------------------------
def Fibonacci_2( number_of_values: int) -> list:
    def fib_generator(n: int) -> int:
        a, b = 0, 1
        yield(a)
        for _ in range(number_of_values - 1):
            a, b = b, a+b
            yield(a)
    return( list( fib_generator(number_of_values) ) )

print("\nfunction 2 : using a generator function")
print(Fibonacci_2(20))
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# function 3 : using a recursive function returns the one Fibonacci number 
# in the series specified by argument index_of_value
# as the recursive function returns only the one value specified,
# to get a list of a complete series a list comprehension is used to
# call the function with a range of increasing parameter values    
# ---------------------------------------------------------------------
def Fibonacci_3( index_of_value: int) -> list:
    def fib_recursive(n:int) -> int:
        if n < 2:
            return(n)
        else:
            return(fib_recursive(n - 1) + fib_recursive(n - 2))
    list_fib = [ fib_recursive(index) for index in range(index_of_value) ]
    return(list_fib)

print("\nfunction 3 : using a recursive function")
print(Fibonacci_3(20))
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# function 4 : using same recursive function as previous,
# but made more efficient by using memoization
# a dictionary keeps track of the values already calculated
# if a value was already calculated, it returns the stored answer 
# memo_dictionary will store all values which are calculated once
# the first two fibonacci values can already be stored
# as the recursive function returns only the one value specified
# to get a list of a complete series a list comprehension is used to
# call the function with a range of increasing parameter values    
# ---------------------------------------------------------------------
memo_dictionary = {0:0, 1:1} 
def Fibonacci_4( index_of_value: int) -> list:
    def fib_recursive(n:int) -> int:
        if n in memo_dictionary:
            return( memo_dictionary[ n ] )
        else:
            memo_dictionary[ n ] = fib_recursive(n - 1) + fib_recursive(n - 2)
            return(memo_dictionary[ n ])
    list_fib = [ fib_recursive(index) for index in range(index_of_value) ]
    return(list_fib)

print("\nfunction 4 : using same recursive function with memoization")
print(Fibonacci_4(20))
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# function 5 : the library sympy has a built-in function sympy.fibonacci
# which gives one value in the series specified by the argument
# https://www.sympy.org/
# as the built-in function sympy.fibonacci returns only the one value specified
# to get a list of a complete series a list comprehension is used to
# call the function with a range of increasing parameter values 
# ---------------------------------------------------------------------
from sympy import fibonacci as sympy_fibonacci
def Fibonacci_5( index_of_value: int) -> list:   
    list_of_fibonacci = [ sympy_fibonacci(index) for index in range(20)]
    return(list_of_fibonacci)

print("\nUsing sympy.fibonacci from the sympy library")
print(Fibonacci_5(20))
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# function 6 : Using Binet's formula, a closed-form expression to 
# calculate a number in the fibonacci series directly
# The n-th fibonacci number
#                                  n
#                               phi                   1 + sqrt(5)
# Fn = round_to_nearest_int(  --------  ),     phi = -------------
#                              sqrt(5)                     2
# ---------------------------------------------------------------------
from math import sqrt
sqrt_five = sqrt(5)
phi = ( 1.0 + sqrt_five ) / 2.0

def Fibonacci_6( number_of_values: int) -> list:
    list_fib = []
    for index_of_value in range(number_of_values):
        list_fib.append( int( phi ** index_of_value / sqrt_five + 0.5) )
    return(list_fib)

print("\nUsing Binet's formula, a closed-form expression")
print(Fibonacci_6(20))
# ---------------------------------------------------------------------

