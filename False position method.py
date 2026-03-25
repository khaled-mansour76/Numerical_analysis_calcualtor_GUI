import sympy as sp

def False_Position(func_str, x_lower, x_upper):
    x = sp.symbols('x')
    local_dict = {'pi': sp.pi, 'e': sp.E, 'exp': sp.exp}
    
    try:
        f = sp.sympify(func_str, locals=local_dict)
    except:
        return "Check your function syntax"

    f_lower_val = f.subs(x, x_lower).evalf()
    f_upper_val = f.subs(x, x_upper).evalf()

    if f_lower_val * f_upper_val >= 0:
        return "False Position fails. f(x_lower) and f(x_upper) must have opposite signs."

    lower_bounds = [float(x_lower)]
    upper_bounds = [float(x_upper)]
    intercepts = []
    
    iteration = 0
    tolerance = 0.0001

    while True:
        iteration += 1
        
        a = lower_bounds[-1]
        b = upper_bounds[-1]
        fa = float(f.subs(x, a).evalf())
        fb = float(f.subs(x, b).evalf())
        
        x_intercept = (a * fb - b * fa) / (fb - fa)
        intercepts.append(x_intercept)
        
        f_intercept = f.subs(x, x_intercept).evalf()

        if abs(f_intercept) < 1e-10 or (len(intercepts) > 1 and abs(intercepts[-1] - intercepts[-2]) < tolerance):
            break

        if (fa * f_intercept) < 0:
            lower_bounds.append(a)
            upper_bounds.append(x_intercept)
        else:
            lower_bounds.append(x_intercept)
            upper_bounds.append(b)

    print(f"Root found: {intercepts[-1]}")
    print(f"Total iterations: {iteration}")

func_str = "cos(x) - 3*x + 5" 
False_Position(func_str, 0, sp.pi)