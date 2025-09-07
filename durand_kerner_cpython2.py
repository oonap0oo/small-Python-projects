# Durand–Kerner for quadratic equations

# equation has 4 coefficients a,b,c,d
#   x**4 + a * x**3 + b * x**2 + c * x + d = 0
# has 4 roots: p,q,r,s
#  (x-p)(x-q)(x-r)(x-s) = 0

# f(x) = x**4 + a * x**3 + b * x**2 + c * x + d
# iterating this:
#   pnew = p - f(p)/[(p - q)(p - r)(p - s)]
#   qnew = p - f(q)/[(q - pnew)(q - r)(q - s)]
#   rnew = r - f(r)/[(r - pnew)(r - qnew)(r - s)]
#   snew = s - f(s)/[(s - pnew)(s - qnew)(s - rnew)]
# until p,q,r,s change less then desired precision
#
# initial values for p,q,r,s:
#   p = (0.4+0.9)**0
#   q = (0.4+0.9)**1
#   r = (0.4+0.9)**2
#   s = (0.4+0.9)**3

from cmath import polar
import matplotlib.pyplot as plt

# returns value of polynomial for x
# f(x) = x**4 + a * x**3 + b * x**2 + c * x + d
def poly_value(coeff, x):
    a, b, c, d = coeff
    return x**4 + a * x**3 + b * x**2 + c * x + d

# returns a string showing the equation and coefficient values
def eq_to_str(coeff):
    a, b, c, d = coeff
    txt = "x**4 + a * x**3 + b * x**2 + c * x + d\n"
    txt += f"a = {c_format_rect(a)}, b = {c_format_rect(b)}, c = {c_format_rect(c)}, d = {c_format_rect(d)}"
    return txt

# calculates next interation for Durand–Kerner method
# returns new values for roots p, q, r, s
def durand_kerner_iteration(roots, coeff):
    p, q, r, s = roots
    p_new = p - poly_value(coeff,p) / ( (p - q)*(p - r)*(p - s) )
    q_new = q - poly_value(coeff,q) / ( (q - p_new)*(q - r)*(q - s) )
    r_new = r - poly_value(coeff,r) / ( (r - p_new)*(r - q_new)*(r - s) )
    s_new = s - poly_value(coeff,s) / ( (s - p_new)*(s - q_new)*(s - r_new) )
    return [p_new, q_new, r_new, s_new]

# returns biggest delta between equation residuals with new and old sets of root values
def residual_delta(roots_new, roots_old, coeff):
    max_delta = 0
    for old, new in zip(roots_new, roots_old):
        residual_old = poly_value(coeff, old)
        residual_new = poly_value(coeff, new)
        max_delta = max(max_delta, abs(residual_new - residual_old))
    return max_delta

# loop Durand–Kerner
def durand_kerner_loop(coeff):
    # initial values roots
    # roots = [p, q, r, s]
    base_value = 0.4+0.9j
    roots = [base_value**k for k in range(1,5)]
    # loop
    roots_old = roots
    for loop in range(max_loops):
        roots = durand_kerner_iteration(roots_old, coeff)
        if residual_delta(roots, roots_old, coeff) < max_delta_residual:
            print(f"\n{loop} iterations done, conversion reached")
            break
        roots_old = roots
    else:
        print(f"\nmaximum number of iterations done without reaching conversion")
    return roots

# returns string containing rectangular representation of complex number
def c_format_rect(z):
    if z == 0.0:
        expr = "0.0"
    elif abs(z.real) > abs(z.imag * 1e12): # if imag is very small compared to real, show as real
        expr = f"{z.real:.12}"
    else:
        expr = f"{z.real:.12} {z.imag:+.12}*j"
    return expr

# returns string containing polar representation of complex number
def c_format_polar(z):
    r, phi = polar(z)
    if abs(phi) < 1e-12: # if phi is very small, show as real
        expr = f"{r:.12}" 
    else:
        expr =  f"{r:.12} * exp({phi:.8} * j)"
    return expr

# function returns True if the string is a valid float number
def isfloat(x_str):
    try:
        float(x_str)
    except:
        valid = False
    else:
        valid = True
    finally:
        return valid
    
# function returns True if the string is a valid complex number
def iscomplex(x_str):
    try:
        complex(x_str)
    except:
        valid = False
    else:
        valid = True
    finally:
        return valid

# function retrieves number from user
# repeats input if not valid float or complex number
def input_number(prompt):
    valid = False
    while valid == False:
        answer = input(prompt)
        valid = isfloat(answer)
        if valid == True:
            return float(answer)
        valid = iscomplex(answer)
        if valid == True:
            return complex(answer)
        print(f"{answer} not a valid float or complex number")

# input coefficients of equation, return as list
def input_coeff():
    print("Quadratic equation, Durand Kerner method")
    print("----------------------------------------")
    print("\nx**4 + a*x**3 + b*x**2 + c*x + d = 0\n")
    coeff = []
    for coeff_name in ("a","b","c","d"):
        value = input_number(f"input {coeff_name} = ")
        coeff.append(value)
    return coeff

# print results to console
def print_results(roots):
    print((f"\nRoots of {eq_to_str(coeff)}"))
    for n, root in enumerate(roots):
        rect_str = c_format_rect(root)
        polar_str = c_format_polar(root)
        if rect_str != polar_str:
            print(f"\nx{n} = {rect_str} = {c_format_polar(root)}")
        else:
            print(f"\nx{n} = {rect_str}")
        print(f"abs(Residual) = {abs(poly_value(coeff, root))}")

# plot of roots in complex pane
def plot_roots(roots):
    fig, ax = plt.subplots(figsize=(12, 9), facecolor = "#D0D0D0")
    ax.set_facecolor("#F0F0F0")
    markers = [(k,2,0) for k in range(3,7)]
    for k, root in enumerate(roots):
        x = root.real
        y = root.imag
        #print(f"x={x:<25}\ty={y:<25}")
        ax.scatter(x, y, marker = markers[k], s = 500,
                   linewidths = 3, label = c_format_rect(root))
    ax.legend(fontsize = plot_text_size, framealpha = 0.4)
    ax.minorticks_on()
    ax.set_title(f"Roots of\n{eq_to_str(coeff)}", fontsize = plot_text_size + 2)
    ax.grid(visible = True, which = "major", axis = "both", color = "grey", linestyle = "--", linewidth = 1)
    ax.set_xlabel("real", fontsize = plot_text_size)
    ax.set_ylabel("imaginary", fontsize = plot_text_size)
    ax.tick_params(axis = "both", which = "major", labelsize = plot_text_size)
    ax.tick_params(axis = "both", which = "minor", labelsize = plot_text_size - 2)
    ax.axhline(y=0, linewidth = 2, color = "black", linestyle="--")
    ax.axvline(x=0, linewidth = 2, color = "black", linestyle="--")
    ax.margins(0.25)
    fig.set_edgecolor("#B0B0B0")
    plt.show()



# parameters script
max_delta_residual = 1e-8 # when the residuals change less then this value iterations are stopped
max_loops = 100 # maximum number of iteratons allowed
plot_text_size = 18 # font size for plot

# input coefficients of equation
coeff = input_coeff()

# loop Durand–Kerner, returns list of roots
roots = durand_kerner_loop(coeff)

# show results
print_results(roots)

# plot of roots
input("\n Hit Return for plot of roots in complex pane")
plot_roots(roots)

print("\n...Script finished")

        
