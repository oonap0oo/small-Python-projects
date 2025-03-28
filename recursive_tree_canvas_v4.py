#!/usr/bin/env python3
#
#  recursive_tree_canvas_v4.py
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
#  Drawing recursive trees on a Tkinter canvas. Four different looking
#  trees are drawn using the same code with different parameters
#  function branch() draws one branch and calls function start_new_branches()
#  function start_new_branches() calls branch() three times to draw branches 
#  with different angles. Recursion depth is controlled by parameter number_of_recursions
#
from tkinter import *
from math import *


class Trees(Tk):
    def __init__(self):
        super().__init__()
        
        self.width_img = 1900 # width of the image
        self.height_img = 1000 # height of the image
        
        self.wm_title("Recursive trees on a Tkinter canvas")
        
        # make a canvas widget and position it to cover the window using pack()
        self.C = Canvas(self,width = self.width_img, height = self.height_img, background="black")
        self.C.pack()

        
        # parameters tree 1
        self.list_colors = ("dark blue","blue","cyan","red","orange","yellow","white")
        self.angle_delta = pi / 3 # angle of side brach and main brach
        self.main_branch_length_reduction_ratio = 0.98 # factor used to decrease length of main braches inbetween recursions
        self.side_branch_length_reduction_ratio = 0.5 # factor used to decrease length of side braches inbetween recursions
        self.number_of_recursions = 9 # recursion depth
        self.number_of_recursions_animate = 5 # recursion depth above which to update canvas after each branch draw
        self.branch_length_start = 95 # trunk length
        self.angle_trunk=pi / 2 # angle of the trunk
        self.x_position = 300
        
        # start new tree with the new parameters
        self.start_new_tree()
        
        # parameters tree 2
        self.list_colors = ("red","orange","yellow","lightgreen","green","blue","cyan","magenta","white")
        self.angle_delta = pi / 8 # angle of side brach and main brach
        self.main_branch_length_reduction_ratio = 0.93 # factor used to decrease length of main braches inbetween recursions
        self.side_branch_length_reduction_ratio = 0.9 # factor used to decrease length of side braches inbetween recursions
        self.number_of_recursions = 7 # recursion depth
        self.number_of_recursions_animate = 3 # recursion depth above which to update canvas after each branch draw
        self.branch_length_start = 120 # trunk length
        self.angle_trunk=pi / 2 # angle of the trunk
        self.x_position = 700
        
        # start new tree with the new parameters
        self.start_new_tree() 
        
        # parameters tree 3
        self.list_colors = ("lightgreen","green","blue","cyan","magenta","white")
        self.angle_delta = pi / 10 # angle of side brach and main brach
        self.main_branch_length_reduction_ratio = 0.93 # factor used to decrease length of main braches inbetween recursions
        self.side_branch_length_reduction_ratio = 0.7 # factor used to decrease length of side braches inbetween recursions
        self.number_of_recursions = 7 # recursion depth
        self.number_of_recursions_animate = 3 # recursion depth above which to update canvas after each branch draw
        self.branch_length_start = 130 # trunk length
        self.angle_trunk=pi / 2 # angle of the trunk
        self.x_position = 1100
        
        # start new tree with the new parameters
        self.start_new_tree()       
          
        # parameters tree 4
        self.list_colors = ("#402000","#604000","#806000","#a08000","#c0a000","#e0c020","#ffe040","#ffff60","#ffff80")
        self.angle_delta = pi / 4 # angle of side brach and main brach
        self.main_branch_length_reduction_ratio = 0.7 # factor used to decrease length of main braches inbetween recursions
        self.side_branch_length_reduction_ratio = 0.68 # factor used to decrease length of side braches inbetween recursions
        self.number_of_recursions = 10 # recursion depth
        self.number_of_recursions_animate = 8 # recursion depth above which to update canvas after each branch draw
        self.branch_length_start = 228 # trunk length
        self.angle_trunk=pi / 2 # angle of the trunk
        self.x_position = 1500
        
        # start new tree with the new parameters
        self.start_new_tree()     
       
        
    # draw one branch and start new branches by calling start_new_branches()
    def branch(self, x, y, length, angle, depth, color):
        # end point of branch 
        x_end = x + length * cos(angle) 
        y_end = y - length * sin(angle)
        # draw the branch
        self.C.create_line(x, y, x_end, y_end, fill = color, width = depth, capstyle = ROUND)
        # show image at this point if depth is larger then number_of_recursions_animate
        if depth > self.number_of_recursions_animate:
            self.update()
        # if depth is not zero yet, start another recursion
        if depth > 0:      
            self.start_new_branches(x_end, y_end, length * self.main_branch_length_reduction_ratio, 
            angle, depth - 1)
            
    
    # start new branches by calling branch() three times        
    def start_new_branches(self, x, y, length, angle, depth):
        # use different color for every recursion
        color_index = depth % len(self.list_colors)  
        color = self.list_colors[color_index]
        # start side branch
        self.branch(x, y, length * self.side_branch_length_reduction_ratio, angle - self.angle_delta, depth, 
            color) 
        # continue main branch
        self.branch(x, y, length, angle, depth, color) 
        # start other side branch
        self.branch(x, y, length * self.side_branch_length_reduction_ratio, angle + self.angle_delta, depth, 
            color) 
    
    
    def start_new_tree(self):
        # delete previous image
        #C.delete('all')
        
        # draw the trunk of the tree
        self.C.create_line(self.x_position, self.height_img, self.x_position, 
            self.height_img - self.branch_length_start, 
            fill = self.list_colors[len(self.list_colors) - 1], 
            width = self.number_of_recursions + 1, capstyle = ROUND)
    
        # start first branches
        self.start_new_branches(self.x_position, 
            self.height_img - self.branch_length_start , 
            self.branch_length_start, 
            self.angle_trunk, self.number_of_recursions)
   
   
   
# make an instance of the class and start it's main loop    
trees=Trees()
trees.mainloop()

    




