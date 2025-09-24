# Julia Fractal using only math and tkinter libraries
from tkinter import *
from math import *
# parameters
step = 1 # defines resolutuon vs speed (1: max resolution, slowest)
screen_width = 1600; screen_height = 1000 # image size in pixels
# make tkinter and canvas objects
root = Tk()
root.title("Julia Fractal using Python and Tkinter")
canvas1 = Canvas(root, background = "black",
           height = screen_height, width = screen_width)
canvas1.pack()
# calculation and plotting
c = complex(-0.5125, 0.5213) # complex constant for julia fractal
for x in range(0, screen_width, step):
  re = x / (screen_width - 1) * 3.0 - 1.5
  #re = x / (screen_width - 1) * 1.5 - 0.75 # zoomed in version
  for y in range(0, screen_height, step):
    im = y / (screen_height - 1) * 2.0 - 1.0
    #im = y / (screen_height - 1) * 1.0 - 0.5 # zoomed in version
    z = complex(re, im) # initial value for z
    i = 0 # counter will be measure for how fast z grows
    while abs(z) < 2.0 and i < 1024: # exit loop if |z| > 2.0 or 1024 iterations completed
      z = z**2 + c
      i += 1
    i = int(sqrt(i)*8) # apply non linear scaling on i
    r = i % 33 * 8; r = min(255, r) # calculate color comp. from i
    g = i % 129 * 2; g = min(255, g)
    b = i % 65 * 4; b = min(255, b)
    col_str = f"#{r:02X}{g:02X}{b:02X}" # color in "#rrggbb" format, hex values
    canvas1.create_rectangle(x, y, x + step, y + step,
                             fill = col_str, outline = col_str) # plot ontkinter canvas
  if x % 50 == 0:
    canvas1.update() # each 50 cycles show updated canvas
# plotting finished, window shows
mainloop()
