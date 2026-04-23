import sympy as sp
import pandas as pd
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

def Bisection(func, a_val, b_val, eps=0.0001):
    x = sp.symbols('x')
    local_dict = {'pi': sp.pi, 'e': sp.E, 'exp': sp.exp, 'cos': sp.cos, 'sin': sp.sin, 'tan': sp.tan}
    transformations = standard_transformations + (implicit_multiplication_application,)
    try:
        f = parse_expr(func, local_dict=local_dict, transformations=transformations)
    except Exception as e:
        return f"Check syntax: {str(e)}", None, None
    a_current = float(a_val)
    b_current = float(b_val)
    fa_val = f.subs(x, a_current).evalf()
    fb_val = f.subs(x, b_current).evalf()
    if fa_val * fb_val >= 0:
        return "Bisection fails: f(a) and f(b) must have opposite signs.", None, None
    history = []
    iteration = 0
    tolerance = float(eps)
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
