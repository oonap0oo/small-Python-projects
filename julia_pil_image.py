# Julia Fractal using only math and PIL libraries
# the image is calculated and opened in the system's standard image viewer
# as PNG file
# PIL (Pillow) does not come with a standard CPython installation
# see: https://pypi.org/project/pillow/
#
from PIL import Image, ImageDraw
from math import sqrt
# parameters
screen_width = 1600; screen_height = 1000 # image size in pixels
# create a new PIL Image object
img = Image.new("RGB",(screen_width, screen_height),
                "black")
draw = ImageDraw.Draw(img)
# calculation and plotting
c = -0.4 + 0.6j # complex constant for julia fractal
# other interesting values:
# -0.5125 + 0.5213j, -0.499 + 0.5213j, -0.498 + 0.5213j,
# -0.8 + 0.156, -0.7269 + 0.1889
for x in range(0, screen_width):
    re = x / (screen_width - 1) * 3.2 - 1.6
    for y in range(0, screen_height):
        im = y / (screen_height - 1) * 2.0 - 1.0
        z = complex(re, im) # initial value for z
        for i in range(1025): # counter will be measure for how fast z grows
            z = z**2 + c
            if abs(z) > 2.0:
                break
        i = int(sqrt(i)*8) # apply non linear scaling on i
        r = i % 33 * 8; r = min(255, r) # calculate color comp. from i
        g = i % 129 * 2; g = min(255, g)
        b = i % 65 * 4; b = min(255, b)
        col = (r,g,b)
        draw.point([x, y], fill = col)
    if x % 100 == 0:
        print(f"{x/(screen_width-1):.0%} calculated")    
# plotting finished, image opens in standard img viewer
img.show()
