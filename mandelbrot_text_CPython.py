# Mandelbrot fractal on a text console
# this script uses ansi commands to set colors
# it is designed for text consoles with ansi compatibility

width=180 # width of output in characters
height=52 # height of output in characters
print("\033[01m") # ansi command to set bold characters 
for y in range(height):
    im=y/(height-1)*2.5-1.25 # imaginary part of initial complex number
    for x in range(width//2):
        re=x/(width//2-1)*3.3-2.2 # real part of initial complex number
        c=complex(re,im) # complex number c is vreated
        z=0
        i=0
        while abs(z)<2 and i<255: # loop with c as constant
            z=z**2+c # iteration for mandelbrot
            i+=1 # keep track of number of loops this value is the used result
        if i==255: # print spaces if loop ended without z going to infinity
            print("  ",end="")
        else:
            col=i%8 
            col_txt=f"\033[{30+col}m" # ansi foreground color depends on result
            txt=f"{i:2X}" # hex representation of result
            print(col_txt+txt,end="")
    print() # start new row of text
print("\033[0m") #reset ansi commands
