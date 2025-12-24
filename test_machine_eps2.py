# Determine machine epsilon through test
#
# epsilon is smallest value such that (1.0 + epsilon) is still distinguishable from 1.0 by the system
# (note: for numpy epsilon can also be found directly using numpy.finfo())

import numpy as np

def get_eps(datatype):
    if datatype==float:
        eps=1.0
        x=1.0
    else:
        eps = np.array([1.0], dtype=datatype)
        x = np.array([1.0], dtype=datatype)
    exponent=0
    while True: # loop until half_eps is too small to change value of x
        half_eps = eps / 2.0
        if x == x + half_eps:
            break
        eps = half_eps
        exponent-=1
    if datatype==float:
        print(f"\n{type(x)}:\nepsilon = {eps} = 2**({exponent:.0f})")
        print("1.0 + eps = ",x+eps)
        print("1.0 + eps/2 = ",x+half_eps)
    else:
        print(f"\n{type(x[0])}:\nepsilon = {eps[0]} = 2**({exponent:.0f})")
        print(f"1.0 + eps = ",x[0]+eps[0])
        print(f"1.0 + eps/2 = ",x[0]+half_eps[0])

print("Machine epsilon for various floating point formats")

get_eps(float)
get_eps(np.half)
get_eps(np.single)
get_eps(np.double)
get_eps(np.longdouble)
