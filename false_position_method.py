import sympy as sp
import pandas as pd
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

def False_Position(func_str, x_lower, x_upper, eps=0.0001):
    x = sp.symbols('x')
    local_dict = {'pi': sp.pi, 'e': sp.E, 'exp': sp.exp, 'cos': sp.cos, 'sin': sp.sin, 'tan': sp.tan}
    transformations = standard_transformations + (implicit_multiplication_application,)
    try:
        f = parse_expr(func_str, local_dict=local_dict, transformations=transformations)
    except Exception as e:
        return f"Check syntax: {str(e)}", None, None
    fa_val = f.subs(x, x_lower).evalf()
    fb_val = f.subs(x, x_upper).evalf()
    if fa_val * fb_val >= 0:
        return "Fails: f(a) and f(b) must have opposite signs.", None, None
    history = []
    iteration = 0
    tolerance = float(eps)
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
            "xs": c,
            "f(xs)": fc
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
