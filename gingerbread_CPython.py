# Gingerbread man fractal
from tkinter import *
from math import *

def color(*args):
    if len(args)==1:
        r, g, b  = args[0]
    else:
        r, g, b  = args
    color_str = f"#{r:02x}{g:02x}{b:02x}"
    return color_str

def dist(x1,y1,x2,y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)

def drawgingerbread(N=50000):
    x,y=-0.1,0
    for _ in range(N):
        xold,yold=x,y
        x,y=1-y+abs(x),x
        xscr=int(900*(x+3.5)/12)
        yscr=int(650*(9.5-y)/12)
        c=int(dist(x,y,xold,yold)/12*512)
        g=(c % 32)*8+7
        b=(c % 256)
        r=(c % 128)*2+1
        canvas1.create_rectangle(xscr-2, yscr-2, xscr+2, yscr+2, fill = color(r,g,b)) 
    canvas1.create_text(300, 30, text = "Gingerbread man fractal", fill = "green", font = ("", 18))

# generating a tkinter window with a canvas widget
window = Tk()
canvas1 = Canvas(window, width = 900, height = 700, bg="black")
canvas1.pack()

drawgingerbread()

window.mainloop()
