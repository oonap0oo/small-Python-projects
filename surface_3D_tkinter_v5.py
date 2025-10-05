# 3D Surface plot using Python and tkinter
import tkinter as tk
from tkinter import messagebox as mb
from math import *

# functions to plot
def sinc(x,y):
    r = hypot(x,y)
    z = sin(r) / r if r != 0.0 else 1.0
    return z

def gauss(x,y):
    r = hypot(x,y)
    z = exp(-r**2)
    return z

def sincos(x,y):
    z=sin(x)*cos(y)
    return z

def sinr(x,y):
    r = hypot(x,y)
    z = sin(r)
    return z

def sinxy(x,y):
    r = hypot(x,y)
    z=exp(-1/60*r**2) * (sin(1/5*x*y))
    return z


# make new tkinter and canvas objects
def generate_tk_canvas(height, width):
    print("make tkinter and canvas objects")
    new_tk_root = tk.Tk()
    new_tk_root.title("3D Surface plot using Python and tkinter")
    new_tk_canvas = tk.Canvas(new_tk_root, background = "black",
                        height = height, width = width)
    new_tk_canvas.pack()
    return new_tk_canvas, new_tk_root
    

#plotting function
#fun: function to plot must take 2 arguments, return 1
#xrange,yrange,zrange: tuples with (min,max) value
#txt; text which is added to the plot, optional
def surf(tk_canvas, fun, xrange, yrange, zrange, txt = ""):
    print(f"plotting function {txt}")
    v_shift = 5 # vertical distance lines
    h_shift = 3 # horizontal shift between lines
    z_scale = 450 # scale factor for z values
    border = 40
    h_scale = 15 # pixels between points in horizontal direction
    Nv = 80 # number of points calculated for y axis
    Nh = 80 # number of points calculated for x axis
    y_step = (yrange[1] - yrange[0]) / (Nv - 1)
    x_step = (xrange[1] - xrange[0]) / (Nh - 1)
    zspan = zrange[1] - zrange[0]
    x_screen_lst = [0]*Nh; y_screen_lst = [0]*Nh; c_lst = [0]*Nh
    for v in range(Nv, 0, -1):
        y = yrange[0] + y_step * v
        v_delta = v * v_shift # number of pixels to drop vertically for current line
        h_delta = v * h_shift # number of pixels to shift horizontally for current line
        for h in range(0, Nh):
            x = xrange[0] + x_step * h
            z = (fun(x,y) - zrange[0]) / zspan
            x_screen_lst[h] = h_scale * h + h_delta + border
            y_screen_lst[h] = screen_height - (int(z_scale * z) + v_delta + border)
            c_lst[h] = int(200 - v/Nv*200 + z*250)
            c_lst[h] = max(0, min(c_lst[h], 255))
        if v < Nv:
            for h in range(0, Nh):
                if h > 0:
                    # color in "#rrggbb" format, hex values
                    #col_str = f"#{c_lst[h]:02X}{c_lst[h]:02X}{c_lst[h]:02X}"
                    col_str = f"#00{c_lst[h]:02X}00"
                    tk_canvas.create_polygon(old_x_screen_lst[h], old_y_screen_lst[h],
                                           old_x_screen_lst[h-1], old_y_screen_lst[h-1],
                                           x_screen_lst[h-1], y_screen_lst[h-1],
                                           x_screen_lst[h], y_screen_lst[h],
                                           fill = "black", outline = col_str, width = 1)
        old_x_screen_lst = x_screen_lst.copy()
        old_y_screen_lst = y_screen_lst.copy()
    tk_canvas.create_text(40, 30, text = txt,
                          anchor = "nw", font = ("TkFixedFont",18,"normal"), fill = "#00FF00")
    tk_canvas.update()

    

# parameters
screen_width = 1500; screen_height = 1000 # image size in pixels

# examples
examples = ((sincos, (-pi, pi),(-pi, pi),(-1.5, 1.5),"z = sin(x)*cos(y)"),
            (sinc, (-pi*4, pi*4),(-pi*4, pi*4),(-0.1, 1.0),"z = sin(r)/r"),
            (gauss, (-3, 3),(-3, 3),(0.0, 1.0),"z = exp(-r**2)"),
            (sinr, (-3*pi, 3*pi),(-3*pi, 3*pi),(-1.0, 1.0),"z = sin(r)"),
            (sinxy, (-3*pi, 3*pi),(-3*pi, 3*pi),(-0.7, 0.7),"z = exp(-1/60*r**2)*(sin(1/5*x*y))"))

# make tkinter and canvas objects
canvas1, root1 = generate_tk_canvas(screen_height, screen_width)

for example in examples:
    canvas1.delete('all')
    surf(canvas1, *example)
    answer = mb.askyesno("Continue?", "Continue?")
    if answer == False:
        break

tk.mainloop()
