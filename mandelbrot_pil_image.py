# Mandelbrot Fractal using only math and PIL libraries
from PIL import Image, ImageDraw
# parameters
screen_width = 1500; screen_height = 1000 # image size in pixels
# a new PIL Image object
img = Image.new("RGB",(screen_width, screen_height),
                "black")
draw = ImageDraw.Draw(img)
# calculation and plotting
for x in range(0, screen_width):
    re = x / (screen_width - 1) * 3.2 - 2.3
    for y in range(0, screen_height):
        im = y / (screen_height - 1) * 2.4 - 1.22
        c = complex(re, im) # value for c
        z = 0.0
        for i in range(256): # counter will be measure how fast z grows
            z = z**2 + c
            if abs(z) > 2.0:
                break
        i_mod = i % 17 * 16; i_mod = min(255, i_mod)
        col = (i,i,i_mod)
        draw.point([x, y], fill = col) # add the point  on the image
    if x % 100 == 0:
        print(f"{x/(screen_width-1):.0%} calculated")
# plotting finished, image opens in standard img viewer
img.show()
