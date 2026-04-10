import sympy as sp
import pandas as pd

def Bisection(func, a_val, b_val):
    x = sp.symbols('x')
    local_dict = {'pi': sp.pi, 'e': sp.E, 'exp': sp.exp}
    
    try:
        f = sp.sympify(func, locals=local_dict)
    except:
        return "Check your function syntax", None, None

    a_current = float(a_val)
    b_current = float(b_val)

    fa_val = f.subs(x, a_current).evalf()
    fb_val = f.subs(x, b_current).evalf()

    if fa_val * fb_val >= 0:
        return "Bisection fails: f(a) and f(b) must have opposite signs.", None, None

    history = []
    iteration = 0
    tolerance = 0.0001
    prev_c = None

    while True:
        iteration += 1
        
        c = (a_current + b_current) / 2
        fc = float(f.subs(x, c).evalf())
        
        history.append({
            "Iteration": iteration,
            "a": a_current,
            "b": b_current,
            "c (Midpoint)": c,
            "f(c)": fc
        })

        if abs(fc) < 1e-10 or (prev_c is not None and abs(c - prev_c) < tolerance):
            break

        fa_current = float(f.subs(x, a_current).evalf())
        if fa_current * fc < 0:
            b_current = c
        else:
            a_current = c
            
        prev_c = c
        
        if iteration > 100: 
            break

    df = pd.DataFrame(history)
    
    return c, iteration, df
