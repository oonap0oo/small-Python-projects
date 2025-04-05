#!/usr/bin/env python3
#
#  sierpinski_triangle_tkinter_v6.py
#  
#  Copyright 2025 Kurt Moerman <nap0@nap0-lenovo>
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
# Sierpinski Triangle constructed using the Chaos game method
from tkinter import *
import random as rd
import math

class Sierpinski(Tk):
    def __init__(self):
        # execute init of Tk
        super().__init__()
        # seed the random generator
        rd.seed()        
        # width of the image
        self.width_img = 1024 
        self.half_width = self.width_img // 2
        # height of the image
        self.height_img = 768
        self.half_height = self.height_img // 2
        # window title
        self.wm_title("Sierpinski Triangle on a Tkinter canvas")
        # make a canvas widget and position it to cover the window using pack()
        self.C = Canvas(self,
            width = self.width_img, 
            height = self.height_img,
            background="black")
        self.C.pack()
        self.resizable(False, False)
        
        # number of iterations
        self.N = 20000
        # vertrexes of trangle before scaling starts
        self.x_vertrex = (-50, 0, 50)
        self.y_vertrex = (-30, 50, -30)
        # x and y variables with start value
        x_current = 500
        y_current = 0
        # colors to use, black is only for initial values
        self.colors = ["red","blue","yellow","black"]
        # angle step for rotation, calc sin and cos here once and use variables from there
        self.angle_step = math.radians(7)
        self.angle_cos = math.cos(self.angle_step)
        self.angle_sin = math.sin(self.angle_step)
        # scale step for zooming in and out
        self.scale_steps = (1.05, 1.0 / 1.05)
        self.scale_direction = 0
        self.scale_step = self.scale_steps[self.scale_direction]
        # random number which denotes the vertrex to use and the previous ones in a list
        chosen_vertrex = [3] * 4
        # endless outer loop
        while True: 
            # loop which does 1 zooming-in or zooming-out session
            for _ in range(55):
                # delete previous picture
                self.C.delete('all')
                # loop to draw one triangle
                for index in range(self.N):
                    # new random vertrex out of 3 and keep 3 previous ones
                    chosen_vertrex = [rd.randint(0,2)] + chosen_vertrex[0:3]
                    # calculate new float versions of x and y
                    x_current = 0.5 * (self.x_vertrex[chosen_vertrex[0]] + x_current)
                    y_current = 0.5 * (self.y_vertrex[chosen_vertrex[0]] + y_current)
                    # integer versions with flip in y direction
                    x_plot = int(x_current) + self.half_width
                    y_plot = self.half_height - int(y_current)
                    # using rectangle width and height of 1 seems to give a pixel
                    self.C.create_rectangle(
                        x_plot , y_plot ,
                        x_plot , y_plot ,
                        #fill = self.colors[chosen_vertrex[3]],
                        outline = self.colors[chosen_vertrex[3]]) 
                # cycling though colors not used here
                #self.colors = self.colors[1:] + [self.colors[0]]
                # rotate and scale the coord. of the 3 vertrexes of the triangle
                self.rotation_and_scale()
                # whow newly draw triangle
                self.C.update()                    
            # flip direction between zooming-in and zooming-out
            self.scale_direction = 1 if self.scale_direction == 0 else 0
            # select scaling factor matching the direction
            self.scale_step = self.scale_steps[self.scale_direction]
    
    # rotate and scale the 3 vertrexes of the triangle
    def rotation_and_scale(self):  
        new_x_vertrex = []
        new_y_vertrex = []   
        # apply rotation matrix and scaling factor to the x,y values of the vertrexes   
        for x,y in zip(self.x_vertrex, self.y_vertrex):
            new_x_vertrex.append( (x * self.angle_cos - y * self.angle_sin) * self.scale_step )
            new_y_vertrex.append( (x * self.angle_sin + y * self.angle_cos) * self.scale_step )
        self.x_vertrex = new_x_vertrex 
        self.y_vertrex = new_y_vertrex
 
# make an instance of the class and start it's main loop    
sierpinski = Sierpinski()
sierpinski.mainloop()



