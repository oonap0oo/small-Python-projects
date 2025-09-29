# bifurcation diagram of logistic map
# https://en.wikipedia.org/wiki/Logistic_map
# https://en.wikipedia.org/wiki/Bifurcation_diagram
# the diagram is plotted using tkinter which comes with CPython
# the diagram can be saved as PNG file using PIL (Pillow)
# https://pypi.org/project/pillow/
#
import tkinter as tk
from tkinter import messagebox as mb
from PIL import Image, ImageDraw

# parameters
screen_width = 1600; screen_height = 1000 # image size in pixels
file_name = "logistic_map_python.png" # file name for PNG 
a_start = 3.5; a_end = 4.0 # interval parameter a
log_map_scale_factor = 15 # makes map appear brighter
number_iterations = 2000 # number of iterations on logistic formula
# make tkinter and canvas objects
root = tk.Tk()
root.title("Logistic map using Python and Tkinter")
canvas1 = tk.Canvas(root, background = "black",
           height = screen_height, width = screen_width)
canvas1.pack()
# create a new PIL Image object
img = Image.new("RGB",(screen_width, screen_height), "black")
draw = ImageDraw.Draw(img)
# calculating and plotting logistic map
a_span = a_end - a_start
for x in range(screen_width):
    a = a_start + a_span * x / (screen_width - 1) 
    z = 0.5
    log_map_lst = [0] * screen_height 
    for _ in range(number_iterations):
        z = a * z *(1 - z)
        log_map_lst[ int(z * (screen_height - 1)) ] += 1
    for y in range(screen_height):
        col = min(255, log_map_lst[y] * log_map_scale_factor) 
        col_str = f"#{col:02X}{col:02X}{col:02X}" 
        canvas1.create_line(x, screen_height - y - 1, x + 1, screen_height - y - 1,
                            fill = col_str)
        col_tuple = (col,col,col) 
        draw.point([x, screen_height - y - 1], fill = col_tuple) 
    if x % 50 == 0:
        canvas1.update() # each 50 cycles show updated canvas
# plotting finished, window shows
canvas1.update()
# optionally save as image file
answer = mb.askquestion("Save as image?", f"Save as {file_name}?")
if answer == "yes":
    img.save(file_name, "PNG")
    print(f"Image saved as {file_name}")

tk.mainloop()


