# Orbits
# 2D simulation of object in orbit around earth
#
from math import *
import turtle as tl
import time

# constants
G = 6.6743015e-11 # m³/(kg.s²) Gravitational constant 
m_earth = 5.97219e24 # kg mass of earth
G_times_m_earth = G*m_earth # m³/s² for faster calculation
h_geostat = 35786e3 # m height of geostationary orbit above equator
r_earth = 6378.137e3 # m radius of earth at equator
v_geostat = 3.07e3 # m/s speed for geostationary orbit

# parameters
N_points = 10000 # number of points to calculate for 1 orbit
scale = 1.2e5 # scale factor relates physical distances to size of image in pixels
color1 = "limegreen" #colors for the three types of orbits
color2 = "red"
color3 = "yellow"

# Newton's law of universal gravitation
# F = G * m1 * m2 / r**2
# On an object in orbit
# F_attraction = - G * mass_earth * mass_object / r_distance**2
# (F in opposite direction of r)
#
# Newton's second law of motion
# F = m.a => a = F / m
# => a_object = F_attraction / mass_object
#
# acelleration due to gravity
# => a_object = - G * mass_earth / r_distance**2

# function returns acceleration due to gravity at given position x,y
# x and y components of acceleration are returned
def accel(x,y):
    r_square = x**2 + y**2
    r = sqrt(r_square)
    a = -G_times_m_earth / r_square # total acceleration m/s² a = -G*m_earth/r**2
    ax = a * x / r # x and y components of a
    ay = a * y / r
    return ax, ay, r

# print text containing data using turtle
def update_text_data(t, x, y, vx, vy):
    r = sqrt(x**2 + y**2)
    v = sqrt(vx**2 + vy**2)
    minutes, seconds = divmod(t, 60)
    hours, minutes = divmod(minutes, 60)
    txt = f"time = {t:>6.0f} s = {hours:2.0f}h {minutes:2.0f}\" {seconds:2.0f}\'\n\
distance = {r:>10.1f} m = {r/1e3:>7.1f} km\nvelocity = {v:>5.1f} m/s = {v*3.6:>7.1f} km/h"
    text.clear()  # delete only the previous text
    draw_text(text, txt, -700, 350,"white")
    

# calculate and draw 1 trajectory
# initial position x,y and velocity vx,vy are given
# T: total time, here used to calc. dt
# N: number of points to be calculated for trajectory
# col: color to draw in
def draw_traject(x, y, vx, vy, T, N, col):
    tl.color(col)
    tl.penup()
    dt = T/N # time step
    t=0.0
    for k in range(N):
        if k == 1: # 2nd pass
            tl.pendown()
        x_scr = round(x / scale)
        y_scr = round(y / scale)
        tl.goto(x_scr, y_scr)
        # x and y components of acceleration at position x,y
        ax, ay, r = accel(x,y)
        # update x and y components of velocity
        vx += ax * dt; vy += ay * dt
        # update x and y components of position
        x += vx * dt; y += vy * dt
        # update time
        t += dt
        if k % 250 == 0: # each number of steps update text
            update_text_data(t, x, y, vx, vy)
    update_text_data(t, x, y, vx, vy)
    tl.update()
    

# draw text at x,y in given color
# a different turtle instance can be given to
# easily delete just this text afterwards
def draw_text(turtle_instance, txt,x,y,col):
    turtle_instance.pencolor(col)
    turtle_instance.penup()
    turtle_instance.goto(x,y)
    turtle_instance.pendown()
    turtle_instance.write(txt, font = tfont)


# draw earth
def draw_earth():
    tl.penup()
    tl.goto(0, -r_earth/scale)
    tl.color("blue")
    tl.pendown()
    tl.begin_fill()
    tl.circle(r_earth/scale)
    tl.end_fill()

    
# init turtle
#define window size
screen = tl.Screen()
screen.setup(width=1500, height=900)
tl.bgcolor("black")
tl.title("Orbits")
# speed up turtle
tl.speed(0)
tl.tracer(n=2)
# more settings
tl.pensize(5)
tl.hideturtle()
# turtle for text
text = tl.Turtle()
text.hideturtle()
# font to be used
tfont = ("FreeMono", 12, "bold")

# main program
   
# draw earth
draw_text(tl, "Earth", -r_earth / scale * 0.7, -r_earth / scale * 1.5, "blue")
draw_earth()

# Geostationary orbit
draw_text(tl, f"Geostationary orbit", -650, 155, color1)
draw_traject(r_earth + h_geostat, 0,
            0, v_geostat,
            86400 ,N_points, color1)


# Elliptical orbits
draw_text(tl, "Elliptical orbits", 350, -350, color2)
for factor in (0.95, 1.0, 1.05):
    draw_traject((r_earth + h_geostat)*1.9*factor, 0,
                 0, v_geostat*0.35*factor,
                 int(110000*factor), N_points, color2)

# Hyperbolic trajectories
draw_text(tl, "Hyperbolic trajectories", -700, -150, color3)
for factor in (0.95, 1.0, 1.05):
    draw_traject(-(r_earth + h_geostat)*1.8*factor, 0,
                 v_geostat*factor*2.0, -v_geostat*0.6*factor,
                 25000, N_points, color3)

tl.exitonclick()
    


