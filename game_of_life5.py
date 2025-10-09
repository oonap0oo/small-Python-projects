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
# alive = True; dead = False
# neigbours       action if True      action if False
# 0               False               False
# 1               False               False
# 2               True                False  
# 3               True                True
# 4               False               False
# 5               False               False
# 6               False               False
# 7               False               False
# 8               False               False


import tkinter as tk
import numpy as np

# make new tkinter and canvas objects
def generate_tk_canvas(height, width):
    print("make tkinter and canvas objects")
    new_tk_root = tk.Tk()
    new_tk_root.title(txt)
    new_tk_canvas = tk.Canvas(new_tk_root, background = "black",
                        height = height, width = width)
    new_tk_canvas.pack()
    return new_tk_canvas, new_tk_root

# counts the number of neighbours at location row,col in field
# handles wrap around when at a border of the field
def neighbours2(field, row, col):
    # all the row and col indexes to be checked
    rows = [(row-1)%Nrow, row, (row+1)%Nrow]
    cols = [(col-1)%Ncol, col, (col+1)%Ncol]
    # make 3x3 arrays containing row and col indexes
    R,C = np.meshgrid(rows,cols)
    # sum the elements equal to True, do not count the row,col element itself
    n = np.sum(field[R,C]) - field[row, col] 
    return n

# fill field "target" with new values according to the rules
# and based on values in field "source"
def update_field(source, target, gen_count):
    for row in range(Nrow):
        for col in range(Ncol):
            n = neighbours2(source, row, col)
            if n == 2:
                target[row, col] = source[row, col]
            elif n == 3:
                target[row, col] = True
            else:
                target[row, col] = False
    return gen_count+1

# draw graphical representations of "field" on tkinter canvas "cvs"
def drawfield(field, cvs):
    # delete previous
    cvs.delete('all')
    # draw vertical grid lines
    x = 0
    for col in range(Ncol):
        cvs.create_line(x, 0, x, screen_height, fill = grid_color)
        x += dx
    # draw horizontal grid lines
    y = 0
    for row in range(Nrow):
        cvs.create_line(0, y, screen_width, y, fill = grid_color)
        y += dy
    # get row and column indexes of elements in array field equal to True
    rows, cols = np.where(field == True)
    # draw rectangles at locations in grid given by indexes in rows, cols
    for row, col in zip(rows, cols):
        x = col * dx; y = row * dy
        cvs.create_rectangle(x, y, x+dx, y+dy, fill = cell_color, outline = grid_color)
    cvs.create_text(100, 40, text = f"{txt}\nGeneration: {gen_count}",
                    anchor = "nw", font = ("TkFixedFont",18,"normal"), fill = text_color)
    cvs.update()
    
# this functions performs update on one of the field arrays
# and shows new data on the tkinter canvas
# this funtion calls itself after delay "dt"
def update_generation():
    global gen_count, field1, field2 # these global vars have to be modified in this function
    drawfield(field1, canvas1)
    gen_count = update_field(field1, field2, gen_count)
    field1, field2 = field2, field1 # swap arrays, latest one becomes source to calc next one
    root1.after(dt, update_generation)

# stops program after mouse click
def click_handler(event):
    # event also has x & y attributes
    if event.num == 1:
        root1.destroy()
    
    
# parameters
Nrow = 50; Ncol = 75 # number of cells in 2 dimensions
screen_width = 1500; screen_height = 1000 # image size in pixels
dx = int(screen_width / Ncol); dy = int(screen_height / Nrow)
dt = 75 # time delay between steps in milliseconds
txt = "Conway's Game of Life using Python, tkinter and numpy"
grid_color = "#505050"
text_color = "#808080"
cell_color = "red"

# initialise fields
# the fields are numpy arrays of booleans
field1 = np.full((Nrow, Ncol), False, dtype = np.bool_)
field2 = np.full((Nrow, Ncol), False, dtype = np.bool_)

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

# insert patters in field
# adding the patterns to field1 by setting correct elements to True
# adding values to the row or column vectors defines the location in the field
# subtracting a number with the vector flips the orietation of the pattern
field1[gosper_gun_rows+15, gosper_gun_cols+5] = True

# make tkinter root and canvas objects
canvas1, root1 = generate_tk_canvas(screen_height, screen_width)

# define event handler for mouse click
root1.bind("<Button>", click_handler)

# global variable keeps track of number of generations calculated
gen_count = 0

# call this function for the first time, will call itself from then on with time delay
update_generation()

# tkinter main loop
tk.mainloop()

    
