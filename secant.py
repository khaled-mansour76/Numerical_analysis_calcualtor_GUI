import math
import pandas as pd
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor


def secant(f, x0, x1, epsilon=1e-06, max_iter=100):
    xn_1 = float(x0)
    xn = float(x1)
    history = []
    
    for iteration in range(1, max_iter + 1):
        fxn_1 = f(xn_1)
        fxn = f(xn)
        
        denom = fxn - fxn_1
        if abs(denom) < 1e-18: 
            break
            
        approx_dfxn = denom / (xn - xn_1) if (xn - xn_1) != 0 else 1e-18

        xn1  = xn - fxn * (xn - xn_1) / denom
        fxn1 = f(xn1)

        # Store raw float values; the GUI's precision formatter handles display.
        row = {
            'Iteration': int(iteration),
            'xₙ'      : xn,
            'f(xₙ)'   : fxn,
            "f'(xₙ)"  : approx_dfxn,
            'xₙ₊₁'    : xn1,
            'f(xₙ₊₁)' : fxn1
        }
        history.append(row)

        # Convergence check on raw values is more accurate than on rounded snapshots
        if abs(xn1 - xn) < epsilon:
            return xn1, iteration, history 
            
        xn_1 = xn
        xn = xn1
        
    return xn, max_iter, history

def Secant(func, x0, x1, eps=1e-06):
    x = sp.symbols('x')
    local_dict = {'pi': sp.pi, 'e': sp.E, 'exp': sp.exp, 'cos': sp.cos, 'sin': sp.sin, 'tan': sp.tan, 'sqrt': sp.sqrt}
    transformations = standard_transformations + (implicit_multiplication_application, convert_xor)
    try:
        expr = parse_expr(func, local_dict=local_dict, transformations=transformations)
    except Exception as e:
        return (f'Check syntax: {str(e)}', None, None)

    def f(x_val):
        return float(expr.subs(x, x_val).evalf())

    try:
        root, iteration, history = secant(f, x0=float(x0), x1=float(x1), epsilon=float(eps))
        df_table = pd.DataFrame(history)
        return (root, iteration, df_table)
    except Exception as e:
        return (0.0, 0, pd.DataFrame())

if __name__ == '__main__':
    expr_str = "x^3 - 8*x - 5"
    root, n_iter, steps = Secant(func=expr_str, x0=3, x1=3.5, eps=0.00001)
    print(f'Root: {root:.6f}')
    print(steps)