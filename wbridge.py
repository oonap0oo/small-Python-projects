#!/usr/bin/env python3
#
#  wbridge.py
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
# Calculate output voltage of a Wheatstone Bridge as function of one
# variable resisor Rx using Kirchhoff circuit laws and 
# left division operator with a matrix and vector 
circuit = "\n \
    Wheatstone Bridge                                               \n \
         i1    i2                                                   \n \
    o---->--o--<----------o                                         \n \
    |       |             |          Vin = 1V                       \n \
    |       | ^i3         | ^i2                                     \n \
    |       | -         - |          R1 = 1000 Ohm                  \n \
    |       R1            R2         R2 = 1000 Ohm                  \n \
  + o       | +         + |          R3 = 1000 Ohm                  \n \
  Vin       |     Vout    |                                         \n \
  - o    Va o--o -   + o--o Vb                                      \n \
    |       |             |          Vout = ?                       \n \
    |       | -         - |                                         \n \
    |       R3            Rx                                        \n \
    |       | +         + | ^i2                                     \n \
    o-------o-------------o                                         \n \
"
kirchhoff = "\n \
Kirchhoff circuit laws:              \n \
                                    \n \
⎧ i1 + i2 + i3 = 0                  \n \
⎨ Vin + i3.R1 + i3.R3 = 0           \n \
⎩ -i3.R1 + i2.R2 + i2.Rx - i3.R3 = 0\n \
                                    \n \
which means:                        \n \
                                    \n \
⎧ i1 + i2 + i3 = 0                  \n \
⎨ -(R1 + R3).i3 = Vin               \n \
⎩ (R2 + Rx).i2 - (R1 + R3).i3 = 0   \n \
                                    \n \
A*x = b                             \n \
                                    \n \
    | 1      1          1    |      \n \
A = | 0      0      -(R2+R3) |      \n \
    | 0   (R2+Rx)   -(R2+R3) |      \n \
                                    \n \
    |  0  |                         \n \
b = | Vin |                         \n \
    |  0  |                         \n \
                                    \n \
also                                \n \
                                    \n \
Vout = i3.R3 - i2.Rx                \n \
"
print(circuit)
print(kirchhoff)
# import numpy for matrix calculations and matplotlib for plotting
import numpy as np
import matplotlib.pyplot as plt
# ***  Wheatstone Bridge ***
# define circuit values
Vin = 1 ; print(f"Vin = {Vin} V")
R1 = 1e3 ; print(f"R1 = {R1} Ohm")
R2 = 1e3 ; print(f"R2 = {R2} Ohm")
R3 = 1e3 ; print(f"R3 = {R3} Ohm")
# vector of different values in Rx, done this way to give the same values as simulator LTSPICE
Rx = np.append(np.geomspace(100,1e3,num=11)[:-1], np.geomspace(1000,10e3,num=11))
# solve the Kirchhoff equations system for a range of values of Rx
print("Calculated using Python + Numpy")
print("-------------------------------")
print("      Rx(Ohm)      Vout(V)")
Vout = np.zeros(0)
for r in Rx:
    # define the system of equations as Z.I = V
    # all the resistances in matrix Z
    Z = np.array( [[1, 1, 1], [0, 0, -(R2+R3)], [0, (R2+r), -(R2+R3)]] )
    # on the right side of the equal sign, all the voltages in vector V (only 1 here)
    V = np.array([0, Vin, 0]).transpose()
    I = np.linalg.solve(Z, V)
    # calculate Vout from the currents in vector I using dot pruduct
    vout_new = np.dot(I, np.array([0, -r, R3]))
    print(f"{r:>8.2f} Ohm    {vout_new:>8.6f} V")
    Vout = np.append(Vout, vout_new)
print("\n")
# plot values
plt.figure(figsize=(15, 10), num="Python + Numpy Wheatstone Bridge output vs Rx")
plt.title("Python + Numpy\nWheatstone Bridge output vs Rx")
plt.xscale("log")
plt.plot(Rx, Vout)
plt.xlabel("frequency (Hz)", fontsize=15)
plt.ylabel("magnitude (dB)", fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.grid()
plt.show()


    
    
