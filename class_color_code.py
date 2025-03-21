#!/usr/bin/env python3
#
#  class_color_code.py
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
# class resistor()
# contains code to find the value of a resistor 
# out of the color codes present on the component
#
# class resistance()
# contains code to find the colorband colors
# out of the value and tolerance of the component
# both for sets of 4 and 5 colorbands 

class resistor():
    
    # class attributes
    
    dict_colors = {
        "black":0,
        "brown":1,
        "red":2,
        "orange":3,
        "yellow":4,
        "green":5,
        "blue":6,
        "violet":7,
        "grey":8,
        "white":9
        }
        
    # a shallow copy has to be made to avoid modifying the original dictionary
    dict_multiplier_colors = dict_colors.copy()
    dict_multiplier_colors.update({
        "gold":-1,
        "silver":-2
        })
        
    dict_tolerance_colors = {
        "silver":10,
        "gold":5,
        "brown":1,
        "green":0.5,
        "violet":0.1
        }
    
    
    
    
    
    # Dunder methods
    
    # instance initialisation method
    def __init__(self, *args):
        # no argument given
        if len(args) == 0:
            raise Exception(f"no arguments given, expected colors of colorband")
        # one argument given 
        elif len(args) == 1:
            # the 1 argument is a list or tuple 
            if isinstance(args[0], (list, tuple)):
                colorbands = args[0]                
            else:
                raise Exception(f"{args} contains invalid type of argument: {type(args[0])}")
        # seperate arguments given which are strings representing colors
        elif len(args) > 1:
            colorbands = args
        # check if the elements in colorbands are valid    
        self.checkcolorbandsarevalid(colorbands)        
        # if this point is reached all checks are ok
        # assign the list of given colors to instance attribute 
        self.colorbands = colorbands
        
    
    # machine readable representation    
    def __repr__(self):
        colors = ( f"\"{color}\"" for color in self.colorbands)
        colorstr = ",".join(colors)
        return(f"resistor({colorstr})")
        
    # reprsentation as string, shows actual value and tolerance
    def __str__(self):        
        value, tol = self.getvalue()
        valuestr = self.floattometricprefix(value, unit="Ohm")
        return(f"{valuestr} {tol}%")  
        
    def __iter__(self):
        value, tol = self.getvalue()
        yield(value)
        yield(tol)   
        
    def __float__(self):
        value, tol = self.getvalue()
        return(value)
        
    
    # instance methd to check if colorbands are valid
    def checkcolorbandsarevalid(self, colorbands):
        # check the strings representing colors in colorbands for being valid   
        match len(colorbands):            
            case 4:
                for colorband in colorbands[0:2]:
                    if (colorband not in resistor.dict_colors):
                        raise Exception(f"{colorband} not recognised as valid value colorband") 
                if colorbands[2] not in resistor.dict_multiplier_colors:
                    raise Exception(f"{colorbands[2]} not recognised as valid multiplier colorband")
                if colorbands[3] not in resistor.dict_tolerance_colors:
                    raise Exception(f"{colorbands[3]} not recognised as valid tolerance colorband")
            case 5:
                for colorband in colorbands[0:3]:
                    if (colorband not in resistor.dict_colors):
                        raise Exception(f"{colorband} not recognised as valid value colorband") 
                if colorbands[3] not in resistor.dict_multiplier_colors:
                    raise Exception(f"{colorbands[3]} not recognised as valid multiplier colorband")
                if colorbands[4] not in resistor.dict_tolerance_colors:
                    raise Exception(f"{colorbands[4]} not recognised as valid tolerance colorband")
            case _:
                raise Exception(f"{colorbands} contains invalid number of colors: {len(colorbands)}")
            

    # instance method calculate value out of color bands
    # returns tuple with (value, tolerance) as numbers    
    def getvalue(self):
        match len(self.colorbands):
            # 4 colorbands: 2 give value, 1 multiplier, 1 tolerance
            case 4:
                digits = ""
                for digitband in self.colorbands[0:2]:
                    digit = resistor.dict_colors[ digitband ]
                    digits += str(digit) 
                multiplier = "e" + str( resistor.dict_multiplier_colors[ self.colorbands[2] ] )
            # 5 colorbands: 3 give value, 1 multiplier, 1 tolerance
            case 5:
                digits = ""
                for digitband in self.colorbands[0:3]:
                    digit = resistor.dict_colors[ digitband ]
                    digits += str(digit) 
                multiplier = "e" + str( resistor.dict_multiplier_colors[ self.colorbands[3] ] )
        # the last colorband is the tolerance
        tolerance = resistor.dict_tolerance_colors[ self.colorbands[-1] ]
        resistancevalue = float( f"{digits}{multiplier}" )
        return (resistancevalue, tolerance)
        
    
    # static class method, convert a float to string with metric prefix
    @staticmethod
    def floattometricprefix( x , unit="", precision=3 ):   
        dictprefix = {12:"T",9:"G",6:"M",3:"k",-3:"m",-6:"µ",-9:"n",-12:"p",-15:"f"} 
        sci = f"{x:e}"
        mantissastr,exponentstr = sci.split("e")
        newexponent = int(exponentstr) // 3 * 3
        factormantissa=10 ** (int(exponentstr) % 3)
        newmantissa = float(mantissastr) * factormantissa
        newmantissa = round(newmantissa, precision)
        prefix = dictprefix.get(newexponent)
        if prefix is None:
            if newexponent != 0:
                engstr = f"{newmantissa}E{newexponent:+03d} {unit}"  
            else:
                engstr = f"{newmantissa} {unit}"
        else:        
            engstr = f"{newmantissa} {prefix}{unit}"
        return engstr


class resistance():
    
    dict_value_to_colors = {
    0: "black", 
    1: "brown", 
    2: "red", 
    3: "orange", 
    4: "yellow", 
    5: "green", 
    6: "blue", 
    7: "violet", 
    8: "grey", 
    9: "white"
    }
    
    # a shallow copy has to be made to avoid modifying the original dictionary
    dict_multiplier_to_colors = dict_value_to_colors.copy()
    dict_multiplier_to_colors.update(
    {
    -1: "gold",
    -2: "silver"
    })

    dict_tolerance_to_colors = {
    10: "silver", 
    5: "gold", 
    1: "brown", 
    0.5: "green", 
    0.1: "violet"
    }    
    
    # dunder methods
    
    def __init__(self, value, tolerance, number_of_colors = 4):
        if not isinstance(value, (float,int)):
            raise Exception(f"{value} not a valid value")
        if not isinstance(tolerance, (float,int)):
            raise Exception(f"{tolerance} not a valid tolerance")
        if not isinstance(number_of_colors, int):
            raise Exception(f"{number_of_colors} not a valid number of color bands")
        else:
            if (number_of_colors < 4) or (number_of_colors > 5):
                raise Exception(f"{number_of_colors} number of color bands must be 4 or 5")
        self.value = value
        self.tolerance = tolerance
        self.number_of_color_bands = number_of_colors
    
    # machine readable representation    
    def __repr__(self):
        return(f"resistance({self.value},{self.tolerance},{self.number_of_color_bands})")
        
    # representation as string, shows actual colorbands
    def __str__(self): 
        colorsstr = ""
        for colorband in self.getcolorbands():
            colorsstr += f" {colorband} "
        return(colorsstr.strip())
    
    # iterable allows use of list() for example   
    def __iter__(self):
        for colorband in self.getcolorbands():
            yield colorband
    
    # instance method to get colorbands based on value, tolerance and number of bands
    def getcolorbands(self):
        # value as string in scientific notation
        sci = f"{self.value:e}"
        # get mantissa and exponent as strings
        mantissastr,exponentstr = sci.split("e")
        # depending on the number of rings
        match self.number_of_color_bands:
            case 4:
                # get 2 digits and look them up in dictionary to add 2 colors to list colorband
                mantissa = float(mantissastr) * 10
                exponent = int(exponentstr) - 1
                digit = mantissa // 10
                colorband = [resistance.dict_value_to_colors[digit]]
                digit = mantissa - digit * 10
                colorband.append(resistance.dict_value_to_colors[digit]) 
            case 5:
                # get 3 digits and look them up in dictionary to add 3 colors to list colorband
                mantissa = float(mantissastr) * 100
                exponent = int(exponentstr) - 2
                digit = mantissa // 100
                colorband = [resistance.dict_value_to_colors[digit]]
                mantissa = mantissa - digit * 100
                digit = mantissa // 10
                colorband.append(resistance.dict_value_to_colors[digit])                  
                digit = mantissa - digit * 10
                colorband.append(resistance.dict_value_to_colors[digit]) 
            case _:
                # another check for number of color bands, maybe not needed?
                raise Exception(f"{self.number_of_color_bands} not a valid number of color bands")
        # the multiplier color depends on exponent
        colorband.append(resistance.dict_multiplier_to_colors[exponent]) 
        # finallly add the color for tolerance
        colorband.append(resistance.dict_tolerance_to_colors[self.tolerance])                
        return(colorband)
        
# tests of class resistor and resistance

if __name__ == "__main__":
    
    print("Test of resistor class")
    print("========================\n")
    
    print("Valid use")
    print("---------\n")
    
    argumentstuple = (
    ("blue","grey","red","gold"),
    ("yellow","violet","black", "orange", "brown"),
    ("brown","red","blue","gold"),
    (["orange","orange","black","gold"]),
    (["brown","green","black","gold","brown"]),
    (["brown","black","silver","violet"])
    )
    
    for arguments in argumentstuple:
        r1 = resistor( *arguments )
        print( r1.__repr__() )
        print( r1 )
        print("using resistance class, get colors back from value and tolerance:")
        print( resistance( *tuple(r1), len(arguments) ) )
        print()
    
    print("Error conditions")
    print("----------------\n")
    
    badarguments = (
    ("orange","red","black"),
    ("brown","silver","magenta","gold"),
    ("brown","red","black","magenta","gold"),
    ("brown","red","black","orange","yellow"),
    ("orange","orange","black","black","black","gold"),
    (3,5,6,4)        
    )
    
    for badargument in badarguments:
        print("try: resistor(", end="")
        print(*badargument, sep=",", end="")
        print(")")
        try:
            r1 = resistor(*badargument)
        except Exception as e:
            print("Exception:", e)
        finally:
            print()
    
    print("try: resistor()")
    try:
        r1 = resistor()
    except Exception as e:
        print("Exception:", e)
    finally:
        print()
        
    print("Test of resistor class")
    print("========================\n")
    
    print("Valid use")
    print("---------\n")
    
    argumentstuple = (
    (12e6,5,4),
    (12e6,1,5),
    (68e3,5,4),
    (68e3,0.5,5),
    (18,5,4),
    (18,5,5),
    (1,5,4),
    (1.5,5,4),
    (0.15,5,4)
    )
    
    for arguments in argumentstuple:
        r2 = resistance(*arguments)
        print(r2.__repr__())
        print("result:",r2)
        print("using resistor class, get value back from colors:\n",resistor(list(r2)))
        print()
        
    
   
    
    
