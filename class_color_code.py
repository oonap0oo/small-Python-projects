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
#
# object oriented code to find the value of a resistor 
# out of the color codes present on the component

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
    
    # instance initialisation function
    def __init__(self, *args):
        # one argument given which is a list or tuple of strings which represent colors
        if len(args) == 1:
            if isinstance(args[0], (list, tuple)):
                if 4 <= len(args[0]) <= 5:
                    colorbands = args[0]
                else:
                    raise Exception(f"{args[0]} contains invalid number of colors: {len(args[0])}")
            else:
                raise Exception(f"{args} contains invalid type of argument: {type(args[0])}") 
        
        # 4 or 5 seperate arguments given which are strings representing colors
        elif 4 <= len(args) <= 5:
            colorbands = args
        else:    
            raise Exception(f"{args} contains invalid number of colors: {len(args)}")
        
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
        
        
        
# tests of class resistance

if __name__ == "__main__":
    
    print("Test of resistance class")
    print("========================\n")
    
    print("Valid use")
    print("---------\n")
        
    r1 = resistor("blue","grey","red","gold")
    print( r1.__repr__() )
    print( r1 )
    print()
                
    r1 = resistor("yellow","violet","black", "orange", "brown")
    print( r1.__repr__() )
    print(r1)
    print()
    
    r1 = resistor("brown","red","blue","gold")
    print( r1.__repr__() )
    print(r1)
    print()
    
    r1 = resistor(["orange","orange","black","gold"])
    print( r1.__repr__() )
    print(r1)
    print()
    
    r1 = resistor(["brown","green","black","gold","brown"])
    print( r1.__repr__() )
    print(r1)
    print()
    
    r1 = resistor(["brown","black","silver","violet"])
    print( r1.__repr__() )
    print(r1)
    print()
    
    print("Error conditions")
    print("----------------\n")
    
    badarguments = (
    ["orange","red","black"],
    ["brown","silver","magenta","gold"],
    ["brown","red","black","magenta","gold"],
    ["brown","red","black","orange","yellow"],
    ["orange","orange","black","black","black","gold"],
    )
    for badargument in badarguments:
        print("try: resistor(" + str(badargument) + ")")
        try:
            r1 = resistor(badargument)
        except Exception as e:
            print("Exception:", e)
        finally:
            print()
        
 
