# Koch Snowflake and Antisnowfalke

import turtle as tl

# draw a Koch Curve using recursion
# is used for 1 side of the figure
def draw_koch_curve(length, recursion_depth, draw_anti_snowflake):
    if recursion_depth > 0:
        length_3 = length / 3
        draw_koch_curve(length_3, recursion_depth - 1, draw_anti_snowflake)
        tl.left(-60 if draw_anti_snowflake else 60)
        draw_koch_curve(length_3, recursion_depth - 1, draw_anti_snowflake)
        tl.right(-120 if draw_anti_snowflake else 120)
        draw_koch_curve(length_3, recursion_depth - 1, draw_anti_snowflake)
        tl.left(-60 if draw_anti_snowflake else 60)
        draw_koch_curve(length_3, recursion_depth - 1, draw_anti_snowflake)
    else:
        tl.forward(length)

# draw the complete snowflake or antisnowflake, uses function draw_koch_curve()
def draw_koch_snowflake(center_xy, length_side, recursion_depth, draw_anti_snowflake):
    xc, yc = center_xy
    y_upper = yc + length_side *0.5
    tl.penup()
    tl.goto(xc, y_upper)
    tl.setheading(-60)
    tl.begin_fill()
    tl.pendown()
    draw_koch_curve(length_side, recursion_depth, draw_anti_snowflake)
    tl.right(120)
    draw_koch_curve(length_side, recursion_depth, draw_anti_snowflake)
    tl.right(120)
    draw_koch_curve(length_side, recursion_depth, draw_anti_snowflake)
    tl.penup()
    tl.end_fill()
    fig_name = "Antisnowflake" if draw_anti_snowflake else "Snowflake"
    tl.goto(-470,370)
    tl.write(f"Koch {fig_name}", align = "center", font = (None, 15, "normal"))
    tl.goto(470,370)
    tl.write(f"Recursion depth = {depth}", align = "center", font = (None, 15, "normal"))
    tl.update()
    tl.title(f"Koch {fig_name}    Recursion depth = {depth}")
    
# setup Turtle               
def init_turtle():
    #define window size
    screen = tl.Screen()
    screen.setup(width=screen_width, height=screen_height)
    screen.colormode(255)
    tl.speed(0)
    tl.pensize(2)
    tl.tracer(0)
    tl.hideturtle()
    tl.bgcolor("#60A0FF")
    tl.pencolor("white")
    tl.fillcolor("#80B0FF")

# clear screen and draw next figure
# function is called repeteatdly using the turtle timer function
def update():
    global depth, draw_anti_snowflake
    tl.clear()
    center = (0,-40) if draw_anti_snowflake else (0,60)
    size = 1000 if draw_anti_snowflake else 825
    draw_koch_snowflake(center, size, depth, draw_anti_snowflake)
    if depth < max_depth:
        depth = depth + 1
    else:
        depth = min_depth
        draw_anti_snowflake = not draw_anti_snowflake
    tl.ontimer(update, time_delay_ms) # set timer for next update


# parameters
screen_width = 1500
screen_height = 1000
time_delay_ms = 1000
max_depth = 6
min_depth = 0


# setup turtle
init_turtle()

# set depth to starting value
depth = min_depth

draw_anti_snowflake = False

# first time call update here
# update() is then called repeatedly using the turtle timer function
update()

tl.exitonclick()
