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
        
    dict_tolerance_colors = {
        "silver":10,
        "gold":5,
        "brown":1,
        "green":0.5,
        "violet":0.1
        }
    
    # Dunder methods
    
    # instance initialisation function
    def __init__(self, *colorbands):
        if len(colorbands) == 1:
            colorbands = colorbands[0]
        if not (4 <= len(colorbands) <= 5):
            raise Exception(f"invalid number of colors present in {colorbands}") 
            return(None)
        for colorband in colorbands:
            if colorband not in resistor.dict_colors:
                if colorband not in resistor.dict_tolerance_colors:
                    errorstr = f"{colorband} not recognised as valid resistor colorband"
                    raise Exception(errorstr) 
                    return(None)
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
    
    # other instance methods

    # instance method calculate value out of color bands
    # returns tuple with (value, tolerance) as numbers    
    def getvalue(self):
        match len(self.colorbands):
            case 4:
                digitbands = self.colorbands[0:2]
                digits = ""
                for digitband in digitbands:
                    digit = resistor.dict_colors[ digitband ]
                    digits += str(digit) 
                    multiplier = "0" * resistor.dict_colors[ self.colorbands[2] ]
            case 5:
                digitbands = self.colorbands[0:3]
                digits = ""
                for digitband in digitbands:
                    digit = resistor.dict_colors[ digitband ]
                    digits += str(digit) 
                    multiplier = "0" * resistor.dict_colors[ self.colorbands[3] ]
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
        
        
        
# tests

if __name__ == "__main__":
    
    r1 = resistor("blue","grey","red","gold")
    print( r1.__repr__() )
    print( r1.getvalue() )
    print( r1 )
    print()
                
    r1 = resistor("yellow","violet","black", "orange", "brown")
    print( r1.__repr__() )
    print( r1.getvalue() )
    print(r1)
    print()
    
    r1 = resistor("brown","red","blue","gold")
    print( r1.__repr__() )
    print( r1.getvalue() ) 
    print(r1)
    print()
    
    r1 = resistor(["orange","orange","black","gold"])
    print( r1.__repr__() )
    print( r1.getvalue() ) 
    print(r1)
    print()
    
