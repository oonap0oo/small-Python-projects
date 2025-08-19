# Trajectory of a projectile with Quadratic drag

# drag proportional to square of velocity
# direction of drag force is opposite of velocity

# drag force and velocity as vectors:
# _____            _
# Fdrag = -k * v * v
# _
# v: vector velocity
# v: scalar velocity

# horizontal and vertical components:
#
# Fdrag_x = -k * v * ( cos(angle) * v )
# Fdrag_y = -k * v * ( sin(angle) * v )
#
# vx = v * cos(angle)
# vy = v * sin(angle)
# v = sqrt(vx**2 + vy**2)
#
# Fdrag_x = -k * v * vx
# Fdrag_y = -k * v * vy

# newton law force and acceleration:
# _        _
# F = m * dv/dt
#
# Fx = m * dvx/dt
# Fy = m * dvy/dt

# x direction
# m * dvx/dt = -k * v * vx
# dvx/dt = - k/m * vx * v

# y direction
# m * dvx/dt = -k * v * vx - g * m
# dvx/dt = - k/m * vx * v - g

# k/m = mu


import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


# this function is used by scipy.solve_ivp() and has to be in the correct format
# including order and type of arguments
# receives value of x,y,vx,vy, parameter mu and time which it does not used as the system
# is time invariant
# returns value of derivatives of x,y,vx,vy
def trajectory(time, variables, mu):
    x, y, vx, vy = variables
    # numpy.hypot(vx, vy) is short for sqrt(vx**2 + vy**2)
    v = np.hypot(vx, vy)
    dx_dt = vx
    dy_dt = vy
    dvx_dt = -mu * vx * v
    dvy_dt = -g - mu * vy * v
    return([dx_dt, dy_dt, dvx_dt, dvy_dt])


# event function used by scipy.solve_ivp() to track zero crossing of y
# and terminate when y becomes negative
def event(time, variables, mu):
    x, y, vx, vy = variables
    return(y)
event.terminal = True # attribute of function, makes solve_ivp() stop when y<0


# calculate series of values for x, y, vx, vy for given initial velocity angle
def calculate(v_angle_deg):
    # calculate x and y components of initial velocity
    v_angle_rad = np.radians(v_angle_deg)
    vx_init = v_total * np.cos(v_angle_rad)
    vy_init = v_total * np.sin(v_angle_rad)
    print(f"v_angle_deg = {v_angle_deg}°")
    print(f"vx_init = {vx_init}")
    print(f"vy_init = {vy_init}\n")
    # set initial conditions    
    variables_initial = [x_init, y_init, vx_init, vy_init]    
    # prepare a tuple with the time interval, an mandatory argument for the scipy function
    time_interval = (0.0, total_time)
    # prepare a numpy ndarray with the time points to be used
    time_points = np.linspace(0, total_time, number_of_steps)
    # --- calculation ---
    # call the scipy function which returns a specific object, here referenced by result
    # additional arguments for function trajectory() have to be passed via a tuple as
    # keyword parameter 'args'
    result = solve_ivp(trajectory, time_interval, variables_initial, t_eval=time_points,
                       args=(mu,), events = event)
    return result


# plot values contained in object result given als argument
def plot_result(v_angle_deg, plot_number, result):
    # unpack the calculated values from the result object
    x_values, y_values, vx_values, vy_values = result.y
    t_values = result.t
    # subplot for trajectory
    plt.subplot(2,1,1)
    # plot trajectory
    label_txt = f"initial angle = {v_angle_deg} degrees"
    plt.plot(x_values, y_values, linewidth = 3, label = label_txt, color = colors[plot_number])
    # annotate plot lines with text showing time points
    txt_step = len(t_values) // 6
    for x, y, value_for_txt in zip(x_values[txt_step::txt_step], y_values[txt_step::txt_step],
                                   t_values[txt_step::txt_step]):
        plt.text(x + 1 ,y, f"{value_for_txt:.2f}s", fontsize = text_size - 2,
        color = colors[plot_number], backgroundcolor = color_plot_background)
    # subplot for velocity
    plt.subplot(2,1,2)
    # plot velocity
    label_txt = f"initial angle = {v_angle_deg} degrees"
    plt.plot(x_values, np.hypot(vx_values, vy_values), linewidth = 3,
             label = label_txt, color = colors[plot_number])



# constants
g = 9.81

# parameters
m = 1.0 # mass in kg
k = 0.01 # Fdrag = - k * v**2
total_time = 15 # in seconds
number_of_steps = 100 # total number of values calculated 
x_init = 0
y_init = 0.1
v_total = 150.0
v_angles_deg = (15.0, 30.0, 45.0, 60.0, 75.0)

# parameter mu calculated out of k and m
mu = k / m

# parameters for the plots
text_size = 16
color_plot_background = "#F0F0F0"
color_background = "#C0C0C0"
colors = list(mcolors.TABLEAU_COLORS)

# create new figure object
fig = plt.figure(figsize = (15, 10), num = "A projectile with Quadratic drag",
                 facecolor = color_background)

# loop for different initial angles
for plot_number, v_angle_deg in enumerate(v_angles_deg):
    # do calculations
    result = calculate(v_angle_deg)
    # abort here if the calculation was not succesfull
    if not result.success:
        print(result.message)
        quit()
    # plot results
    plot_result(v_angle_deg, plot_number, result)  

# subplot for trajectory settings
plt.subplot(2,1,1)
plt.grid(True)
plt.xlabel("x [m]", fontsize = text_size)
plt.ylabel("y [m]", fontsize = text_size)
plt.tick_params(labelsize = text_size)
plt.title("Trajectory of a projectile with Quadratic drag", fontsize = text_size, fontweight = "bold", y = 1.02)
plt.gca().set_facecolor(color_plot_background)
plt.legend(fontsize = text_size - 1)

# subplot for velocity settings
plt.subplot(2,1,2)
plt.grid(True)
plt.xlabel("x [m]", fontsize = text_size)
plt.ylabel("v [m/s]", fontsize = text_size)
plt.tick_params(labelsize = text_size)
plt.title("Velocity of a projectile with Quadratic drag", fontsize = text_size, fontweight = "bold", y = 1.02)
plt.gca().set_facecolor(color_plot_background)
plt.legend(fontsize = text_size - 1)
 
# define space between subplots
plt.subplots_adjust(wspace = 0.2, hspace = 0.293, left = 0.055, right = 0.988, bottom = 0.079, top = 0.96)

# start with plot window maximized, this works at least in linux..
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())


plt.show()


