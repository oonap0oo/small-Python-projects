#!/usr/bin/env python3
#
#  function_sortandfilter_v2.py
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
# function which accepts a list of strings, removes duplicates, sorts alphabetically
# and fiters using a optional search string
def sortandfilter(listofstrings:list, filtertxt:str = "") -> list:
    # convert to set to remove duplicates
    setofstrings = set( listofstrings )
    
    # the key fuction str.casefold lets sorted() sort on lower case strings
    # to sort string purely alphabetically taking not into account whether
    # they start with a capital or small character
    # the strings in the set remain unchanged, sorted() returns a list
    listofstrings = sorted( setofstrings, key=str.casefold )
    
    # define function for use with the filter() statement
    # it returns True if it finds filtertxt in the given string txt
    # works case-insensitive
    def comparetxt(txt:str) -> bool:
        return filtertxt.casefold() in txt.casefold()
    
    # apply filter if filter exists
    # the Python function filter() applies function comparetxt 
    # to all elements in listofstrings, it only retains the elements
    # for which function comparetxt returns True
    if filtertxt != "":
        newlist = list( filter(comparetxt, listofstrings) )
        return newlist
    else:
        return listofstrings
        
        
# test list with Pythons and other snakes contains duplicates            
testdata = [
    "Green tree python",
    "Yellow anaconda",
    "",
    "Boa constrictor",
    "Great Lakes bush viper",
    "Bolivian anaconda",
    "Black Mamba",
    "Death Adder",
    "Green anaconda",
    "Colorado desert sidewinder",
    "Malayan pit viper",
    "Australian scrub python",
    "CPython 3, it can cause headaches",
    "Yellow anaconda",
    "some other snake",
    "Boa constrictor",
    "Royal python",
    "sneaky snakes",
    "Horned viper",
    "Red-tailed boa",
    "Black Mamba",
    "Eastern green mamba",
    "Sonoran sidewinder",
    "Australian scrub python"
    ]

# some tests

print("All Pythons:\n", sortandfilter(testdata, "Python"), end="\n\n")

print("All Anacondas:\n", sortandfilter(testdata, "Anaconda"), end="\n\n")

print("All names containing 'green':\n", sortandfilter(testdata, "green"), end="\n\n")

sortedlist = sortandfilter(testdata)

print("All snakes, sorted and without duplicates:\n", sortedlist, end="\n\n")

print("number of elements in original list: ", len(testdata))   

print("number of elements in sorted list with removed duplicates: ", len(sortedlist))   

        

