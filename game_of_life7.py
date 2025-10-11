#       Conway's Game of Life
#       ---------------------
#
# from Wikipedia:
# ************************************
# Rules
# 
# The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells,
# each of which is in one of two possible states, live or dead (or populated and unpopulated, respectively).
# Every cell interacts with its eight neighbours, which are the cells that are horizontally,
# vertically, or diagonally adjacent. At each step in time, the following transitions occur:
#
#     Any live cell with fewer than two live neighbours dies, as if by underpopulation.
#     Any live cell with two or three live neighbours lives on to the next generation.
#     Any live cell with more than three live neighbours dies, as if by overpopulation.
#     Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
#
# The initial pattern constitutes the seed of the system.
# The first generation is created by applying the above rules simultaneously to every cell in the seed,
# live or dead; births and deaths occur simultaneously,
# and the discrete moment at which this happens is sometimes called a tick.
# [nb 1] Each generation is a pure function of the preceding one.
# The rules continue to be applied repeatedly to create further generations. 
# *************************************
#
# Rules for Game of life per number of neighbours
# alive/occupied = 1;   dead/empty = 0
# n neigbours        | new generation if 1      | new generation if 0
# .................................................................
# 0                  | 0                        | 0
# 1                  | 0                        | 0
# 2                  | 1                        | 0  
# 3                  | 1                        | 1
# 4                  | 0                        | 0
# 5                  | 0                        | 0
# 6                  | 0                        | 0
# 7                  | 0                        | 0
# 8                  | 0                        | 0


import tkinter as tk
import numpy as np

# make new tkinter and canvas objects
def generate_tk_canvas(height, width):
    print("make tkinter and canvas objects")
    new_tk_root = tk.Tk()
    new_tk_root.title(txt)
    new_tk_root.resizable(False, False)
    new_tk_canvas = tk.Canvas(new_tk_root, background = "black",
                        height = height, width = width)
    new_tk_canvas.pack()
    return new_tk_canvas, new_tk_root

# updates values in the field by applying Conway's Game Of Life rules on the existing values
def update_field_vectorized(field):
    # count neighbours by shifting array field in 8 directions with wrap-around using numpy.roll
    # because empty cells are 0, occupied cells are 1, adding the results gives in
    # each cell of the new array neighbours the number of neighbours of that cell in array field
    neighbours = (
        np.roll(np.roll(field,  1, 0),  1, 1) +  # top left
        np.roll(np.roll(field,  1, 0),  0, 1) +  # top
        np.roll(np.roll(field,  1, 0), -1, 1) +  # top right
        np.roll(np.roll(field,  0, 0),  1, 1) +  # left
        np.roll(np.roll(field,  0, 0), -1, 1) +  # right
        np.roll(np.roll(field, -1, 0),  1, 1) +  # bottom left
        np.roll(np.roll(field, -1, 0),  0, 1) +  # bottom
        np.roll(np.roll(field, -1, 0), -1, 1)    # bottom right
    )
    # apply rules of conway's game of life
    # The | operator can be used as a shorthand for np.logical_or on boolean ndarrays
    # The & operator can be used as a shorthand for np.logical_and on boolean ndarrays
    field = (field & (neighbours == 2)) | (neighbours == 3)
    return field, neighbours

# draw graphical representations of "field" on tkinter canvas "cvs"
def drawfield(field, neighbours, cvs):
    # delete previous
    cvs.delete('all')
    # draw vertical grid lines
    for x in x_grid:
        cvs.create_line(x, 0, x, screen_height, fill = grid_color)
    # draw horizontal grid lines
    for y in y_grid:
        cvs.create_line(0, y, screen_width, y, fill = grid_color)
    # get row and column indexes of elements in array field equal to 1
    rows, cols = np.where(field == 1)

    cell_colors = colors[neighbours[rows, cols] % 2]
    # draw rectangles at locations in grid given by indexes in rows, cols
    for y1, x1, y2, x2, cell_color in zip(rows * dx, cols * dy, rows * dx + dx, cols * dy + dy, cell_colors):
        cvs.create_rectangle(x1, y1, x2, y2, fill = cell_color, outline = grid_color)
    cvs.create_text(100, 40, text = f"{txt}\nGeneration: {gen_count}",
                    anchor = "nw", font = ("TkFixedFont",18,"normal"), fill = text_color)
    cvs.update()
    
# this functions performs update on the field array
# and shows new data on the tkinter canvas
# this funtion calls itself after delay "dt"
def update_generation():
    global gen_count, field1, neighbours1
    drawfield(field1, neighbours1, canvas1)
    field1, neighbours1 = update_field_vectorized(field1)
    gen_count += 1
    root1.after(dt, update_generation)

# stops program after mouse click
def click_handler(event):
    global running # this function has to update the bool "running"
    # event also has x & y attributes
    if event.num == 1: # lef mouse button
        if running:
            root1.destroy() # if already running then stop
        else:
            running = True # if not running yet, start
            # call this function for the first time, will call itself from then on with time delay
            update_generation()
    
    
# ------ parameters ------
# number of cells in 2 dimensions
Nrow = 80; Ncol = 120
# image size in pixels
screen_width = 1500; screen_height = 1000 
# spacing between grid lines
dx = int(screen_width / Ncol); dy = int(screen_height / Nrow)
# prepare x and y values at which to draw grid lines
x_grid = np.arange(0, screen_width, dx)
y_grid = np.arange(0, screen_height, dy)
# time delay between steps in milliseconds
dt = 30
# title text
txt = "Conway's Game of Life using Python, tkinter and numpy"
# define colors to use
grid_color = "#303030"
text_color = "#808080"
#cell_color = "red"
colors = np.array(("red","orange"))


# initialise field
# the field is a numpy array of integers
# 0: dead/empty
# 1: alive/occupied
field1 = np.zeros((Nrow, Ncol), dtype = np.ubyte)
neighbours1 = np.zeros((Nrow, Ncol), dtype = np.ubyte)

# patterns
# some known patters are defined here as 2 numpy arrays containing
# their row and column index values
# a "blinker", stationary
blinker_rows = np.array((0,1,2))
blinker_cols = np.array((0,0,0))
# a "toad", stationary
toad_rows = np.array((1,1,1,0,0,0))
toad_cols = np.array((0,1,2,1,2,3))
# a "glider", moves diagonally
glider_rows = np.array((1,2,2,1,0))
glider_cols = np.array((0,1,2,2,2))
# a "gosper's gun", complicated machine which generates moving "gliders" 
gosper_gun_rows = np.array((5,5,6,6, 5, 6, 7, 4, 8, 3, 9, 3, 9, 6, 4, 8, 5, 6, 7, 6, 3, 4, 5, 3, 4, 5, 2, 6, 1, 2, 6, 7, 3, 4, 3, 4))
gosper_gun_cols = np.array((1,2,1,2,11,11,11,12,12,13,13,14,14,15,16,16,17,17,17,18,21,21,21,22,22,22,23,23,25,25,25,25,35,35,36,36))
# single line infinite growth pattern
single_line_rows = np.array((0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,))
single_line_cols = np.array((1,2,2,3,4,5,6,7,8,10,11,12,13,14,18,19,20,27,28,29,30,31,32,33,35,36,37,38,39))
# single block-laying switch engine
block_layer_rows = np.array((0,0,0,0,1,2,2,3,3,3,4,4,4))
block_layer_cols = np.array((0,1,2,4,0,3,4,1,2,4,0,2,4))


# insert patterns in field
# adding the patterns to field1 by setting correct elements to 1
# adding values to the row or column vectors defines the location in the field
# subtracting a number with the vector flips the orientation of the pattern
field1[gosper_gun_rows+10, gosper_gun_cols+5] = 1
field1[gosper_gun_rows+10, 118-gosper_gun_cols] = 1


# make tkinter root and canvas objects
canvas1, root1 = generate_tk_canvas(screen_height, screen_width)

# define event handler for mouse click
root1.bind("<Button>", click_handler)

# global variable keeps track of number of generations calculated
gen_count = 0

running = False


# tkinter main loop
tk.mainloop()

    
