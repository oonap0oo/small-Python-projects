# recursive turtle drawing Sierpinsky Triangle
import turtle as tl
import time

# function which draws text at x,y position using turtle
def text(txt,x,y,font_size=16):
    tl.color("black")
    tl.penup()
    tl.goto(x,y)
    tl.write(txt,align="center",font=("Sans",font_size,"normal"))

# calculates the x,y of the point exactly in middle of 2 given points
def midpoint(p1,p2):
    x1,y1=p1;x2,y2=p2
    return [(x1+x2)/2,(y1+y2)/2]

# recursively called function calls itself with 3 smaller triangles if
# recursion depth limit is not reached
# if recursion depth limit is reached, draw a filled rectangle
# points p1,p2,p3 are tuples of (x,y) coordinates
# depth is the number of recursive function calls
# c is the color which will be used at final recursion call
def triangle(p1,p2,p3,depth,c):
    if depth==0: # recursion limit is reached, draw filled triangle
        tl.color(c)
        tl.penup()
        tl.goto(p1[0],p1[1])
        tl.pendown()
        tl.begin_fill()
        tl.goto(p2[0],p2[1])
        tl.goto(p3[0],p3[1])
        tl.goto(p1[0],p1[1])
        tl.end_fill()
        tl.update() 
    elif depth>0: # recursion limit not reached call function again with 3 smaller triangles
        pn12=midpoint(p1,p2) 
        pn23=midpoint(p2,p3)
        pn31=midpoint(p3,p1)
        triangle(p1,pn12,pn31,depth-1,"red")
        triangle(p2,pn12,pn23,depth-1,"green")
        triangle(p3,pn23,pn31,depth-1,"blue")

#parameters
size=600 # defines size of triangle
y_offset=150 # shifts the triangle upwards to fit screen
recursion_depth=9 # number of times function triangle() will call itself with succesively smaller triangles
#define window size
screen = tl.Screen()
screen.setup(width=0.8, height=0.9)
tl.bgcolor("#e0e0e0")
# speed up turtle
tl.speed(0)
# more settings
tl.pensize(1)
tl.hideturtle()

for current_depth in range(1,recursion_depth):
    tl.clear()
    tl.tracer(n=current_depth*2) # speed up turtle more as complexity rises
    # place some text
    text("Sierpinsky Triangle",-3*size//4,size//2+40)
    text("recursively drawn",-3*size//4,size//2,font_size=12)
    text("using turtle",-3*size//4,size//2-30,font_size=12)
    text(f"recursion depth is {current_depth}",-3*size//4,size//2-60,font_size=12)
    # first call to "triangle()" function which will recursively call itself "recursion_depth" times
    triangle([-size,-size+y_offset],[size,-size+y_offset],[0,size//2+y_offset],current_depth,"black")
    time.sleep(1)
