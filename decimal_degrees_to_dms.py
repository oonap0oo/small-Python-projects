#!/usr/bin/env python3
#
#  decimal_degrees_to_dms.py
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
# convert angle in decimal degrees to DMS
import math

# function takes an angle as float nad returns degrees, minutes, seconds as tuple
def decdeg2dms(angle:float) -> (float,float,float):
    fractional, degrees = math.modf(angle)
    minutes = int(fractional * 60)
    seconds = (fractional * 60 - minutes) * 60
    return (degrees, float(minutes), seconds)
     
# function takes tuple of  degrees, minutes, seconds and returns string representation    
def dms2string(angle:(float,float,float)) -> str:
    degrees, minutes, seconds = angle
    return f"{degrees:0.0f}° {abs(minutes):0.0f}' {abs(seconds):0.2f}\""
    
# test of decdeg2dms(angle:float) -> (float,float,float)
# and dms2string(angle:(float,float,float)) -> str   

waarden=(45.5,0.75,30.125,65.777,12.3456789,-30.25,-12.3456)

for waarde in waarden:
    dms = decdeg2dms(waarde)
    check =  dms[0] + dms[1] / 60 + dms[2] / 3600
    print("original:", waarde, sep="\t\t")
    print("(deg,min,sec) ", dms, sep="\t\t")
    print("as string:" , dms2string(dms), sep="\t\t")
    print("recalculate:", check, sep="\t\t")
    print("-"*20)
    
    
    
