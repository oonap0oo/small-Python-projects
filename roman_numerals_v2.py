#!/usr/bin/env python3
#
#  roman_numerals_v2.py
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
#  This code converts a roman numeral in standard form to an integer

# describing the roman numeral system
thousands = {
"M":1000, "MM":2000, "MMM":3000}
hundreds = {
"C":100, "CC":200, "CCC":300, "CD":400, "D":500,
"DC":600, "DCC":700, "DCCC":800, "CM":900}
tens = {
"X":10, "XX":20, "XXX":30, "XL":40, "L":50,
"LX":60, "LXX":70, "LXXX":80, "XC":90}
units = {
"I":1, "II":2, "III":3, "IV":4, "V":5,
"VI":6, "VII":7, "VIII":8, "IX":9}
roman_numeral_system = (thousands, hundreds, tens, units)

# following function takes a roman number and returns the integer value
def roman_arabic_num(roman_num_as_str:str) -> int:
    # Following function takes a dictionary of roman numerals for a particular decimal place
    # and a string containing the roman number. Tt looks if the string starts with any of the numerals,
    # starting with the longest numeral. If match is found, adds the value of that roman numeral 
    # to the integer to be returned and removes the matched roman numeral from the string, 
    # a copy of the reduced string is also returned 
    def parse_str_using_dict(dict_to_use:dict, str_to_use:str) -> (int, str):
        number = 0
        ordered_keys = list(dict_to_use.keys()) 
        ordered_keys.sort(reverse = True, key = len) # the roman numerals as list from longest to shortest
        for key in ordered_keys:
            # is the roman numeral found at the beginning of the complete roman number?
            if str_to_use.startswith(key): 
                number += dict_to_use[key]
                str_to_use = str_to_use[len(key):]
                break # only one roman numeral per decimal place
        return(number, str_to_use)
    # clean up the string representing the roman number    
    roman_num_as_str = roman_num_as_str.upper().strip()
    # iterate through roman thousands, hundreds, tens and units as contained in the dictionaries 
    arabic_number = 0
    for dict_decimal_place in roman_numeral_system:
        number, roman_num_as_str = parse_str_using_dict(dict_decimal_place, roman_num_as_str)
        arabic_number += number # build up the final integer value
    return(arabic_number)



if __name__ == "__main__":
    # dictionary to test the function, "roman number":integer
    test_romans = {
        "XXII":22,
        "XIX":19,
        "LXXXVIII":88,
        "XXXIX":39,
        "CCXLVI":246,
        "DCCLXXXIX":789,
        "MMCDXXI":2421, 
        "CLX":160,
        "CCVII":207,
        "MIX":1009,
        "MLXVI":1066,
        "MDCCLXXVI":1776,
        "MCMXVIII":1918,
        "MCMXLIV":1944,
        "MMXXV":2025,
        "MCMXII":1912,
        "MM":2000,
        "MMMCMXCIX":3999
        }
    
    # looping through the tests, raises error when test fails
    for test_roman in test_romans:
        result = roman_arabic_num(test_roman)
        correct_result = test_romans[test_roman]
        print(f"{test_roman} parses to {result}, correct value is {test_romans[test_roman]}", end = "")
        if result == correct_result:
            print(" -->  Test PASSED")
        else:
            print(" -->  Test FAILED")
            raise ValueError


