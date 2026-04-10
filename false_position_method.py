import sympy as sp
import pandas as pd

def False_Position(func_str, x_lower, x_upper):
    x = sp.symbols('x')
    local_dict = {'pi': sp.pi, 'e': sp.E, 'exp': sp.exp}
    
    try:
        f = sp.sympify(func_str, locals=local_dict)
    except:
        return "Check your function syntax", None, None

    fa_val = f.subs(x, x_lower).evalf()
    fb_val = f.subs(x, x_upper).evalf()

    if fa_val * fb_val >= 0:
        return "Fails: f(a) and f(b) must have opposite signs.", None, None

    history = []
    iteration = 0
    tolerance = 0.0001
    
    a = float(x_lower)
    b = float(x_upper)
    prev_c = None

    while True:
        iteration += 1
        fa = float(f.subs(x, a).evalf())
        fb = float(f.subs(x, b).evalf())
        
        c = (a * fb - b * fa) / (fb - fa)
        fc = float(f.subs(x, c).evalf())
        
        history.append({
            "Iteration": iteration,
            "a": a,
            "b": b,
            "c (Root)": c,
            "f(c)": fc
        })

        if abs(fc) < 1e-10 or (prev_c is not None and abs(c - prev_c) < tolerance):
            break
        
        if fa * fc < 0:
            b = c
        else:
            a = c
        
        prev_c = c
        
        if iteration > 100: 
            break

    df = pd.DataFrame(history)
    return c, iteration, df
