# Electrical field due to 2 point charges
#
#                    |
#                 q1 o          
#                    |          + observation point
#                    |
# -----------------------------------------
#                    |
#                    |
#                 q2 o
#                    |
#
# rq1: vector to point charge 1
# rq2: vector to point charge 2
# ro: vector to observation point
# r1o: vector from point charge 1 to observation point o
# r2o: vector from point charge 2 to observation point o
#
# ro = rq1 + r1o
# => r1o = ro - rq1
# r2o = ro - rq2
#
# q1:  charge value of point charge 1
# q2:  charge value of point charge 2
# εo: permittivity of a vacuum,
#     8.854 x 10⁻¹² F/m (Farads per meter)
# E(ro): electric field at observation point ro
#
# Electrical field at ro:
# E = 1/(4*pi*εo) * (r1o * q1 / |r1o|³  +  r2o * q2 / |r2o|³) 
#
#
# | x1o = xo - xq1
# | y1o = yo - yq1
#
# | x2o = xo - xq2
# | y2o = yo - yq2
#
# | Ex = 1/(4*pi*εo) * ( (xo - xq1) * q1 / |ro - rq1|³  +  (xo - xq2) * q2 / |ro - rq2|³ ) 
# | Ey = 1/(4*pi*εo) * ( (yo - yq1) * q1 / |ro - rq1|³  +  (yo - yq2) * q2 / |ro - rq2|³ )
#
# Electrical potential
# V = 1/(4*pi*εo) * ( q1 / r1o + q2 / r2o )
# V = 1/(4*pi*εo) * ( q1 / (ro - rq1) + q2 / (ro - rq2) )

import numpy as np
import matplotlib.pyplot as plt

# parameters
d = 0.01 # distance point charges from origin
L = 2*d # distance between point charges
q1 = 1; q2 = -1 # value point charges [coulomb]
N = 20 # number of points calculated, result arrays will be N*N
epsilon = 8.854E-12 # [F/m]
#k = 1/(4 * np.pi * epsilon) # physical value
k = 1 # used so E is scaled with 1/(4 * np.pi * epsilon)

# preparing vectors with coordinates of point charges [x, y]
rq1 = np.array([0, +d / 2]) 
rq2 = np.array([0, -d / 2])

# generate X and Y arrays
x = np.linspace(-L, L, N)
y = np.linspace(-L, L, N)
X,Y = np.meshgrid(x,y)

# prepare arrays for x and y components of E 
Ex = np.zeros([N,N])
Ey = np.zeros([N,N])

# prepare array for V,V will be limted to Vmax
V = np.zeros([N,N])
Vmax = 100

# function calculates x and y components of E
# argument of function is vector ro with 2 coordinates
# np.linalg.norm() gives the magnitude of the vector in this case
def calc_E(ro):
    Ex = k * ( (ro[0] - rq1[0]) * q1 / np.linalg.norm(ro - rq1)**3
               +  (ro[0] - rq2[0]) * q2 / np.linalg.norm(ro - rq2)**3 )
    Ey = k * ( (ro[1] - rq1[1]) * q1 / np.linalg.norm(ro - rq1)**3
               +  (ro[1] - rq2[1]) * q2 / np.linalg.norm(ro - rq2)**3 )
    return Ex, Ey

# function calculates V
# argument is vector ro with 2 coordinates
def calc_V(ro):
    Vt = k * ( q1 / np.linalg.norm(ro - rq1) + q2 / np.linalg.norm(ro - rq2) )
    return Vt

# calling calc_E() and calc_V() for each point
for row in range(N):
    for column in range(N):
        ro = np.array([X[row,column], Y[row,column]])
        Ex[row,column], Ey[row,column] = calc_E(ro)
        V[row,column] = calc_V(ro)

# calculating array containing magnitude of E
E = np.sqrt(Ex**2 + Ey**2)

# limiting V to +-Vmax to aid contour plot
V = np.clip(V, -Vmax, Vmax)

# plotting
plt.rcParams.update({'font.size': 15})
plt.figure(figsize=(11, 9))
plt.quiver(X, Y, Ex/E, Ey/E)
plt.contour(X, Y, V, levels = 15)
plt.scatter(rq1[0], rq1[1], marker = "o", color = "red")
plt.scatter(rq2[0], rq2[1], marker = "o", color = "blue")
plt.title("Electric field / (1/(4*pi*εo)) [V/m]\nElectric potential [V]")
plt.xlabel("E/(1/(4*pi*εo)) [V/M]\nV [V]")
plt.ylabel("E/(1/(4*pi*εo)) [V/M]\nV [V]")
plt.show()





