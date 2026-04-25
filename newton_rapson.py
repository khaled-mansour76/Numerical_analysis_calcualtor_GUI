import math
import pandas as pd
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

def newton_raphson(f, df, x0, epsilon=1e-06, max_iter=100):
    xn = float(x0)
    history = []
    
    for iteration in range(1, max_iter + 1):
        fxn = f(xn)
        dfxn = df(xn)
        
        if dfxn == 0:
            raise ValueError(f'Derivative is zero at x = {xn:.6f}.')
        
        xn1  = xn - fxn / dfxn
        fxn1 = f(xn1)

        # Store raw float values; the GUI's precision formatter handles display.
        # This avoids false-precision artifacts when the user requests more
        # than 6 significant figures.
        row = {
            'Iteration': int(iteration),
            'xₙ'      : xn,
            'f(xₙ)'   : fxn,
            "f'(xₙ)"  : dfxn,
            'xₙ₊₁'    : xn1,
            'f(xₙ₊₁)' : fxn1
        }
        history.append(row)

        # Convergence check on raw values is more accurate than on rounded snapshots
        if abs(xn1 - xn) < epsilon or abs(fxn1) < epsilon:
            return (xn1, iteration, history)

        xn = xn1

    return (xn, max_iter, history)
def Newton_Raphson(func, x0, eps=1e-06):
    x = sp.symbols('x')
    local_dict = {'pi': sp.pi, 'e': sp.E, 'exp': sp.exp, 'cos': sp.cos, 'sin': sp.sin, 'tan': sp.tan, 'sqrt': sp.sqrt}
    transformations = standard_transformations + (implicit_multiplication_application, convert_xor)
    try:
        expr = parse_expr(func, local_dict=local_dict, transformations=transformations)
    except Exception as e:
        return (f'Check syntax: {str(e)}', None, None)
    expr_prime = sp.diff(expr, x)

    def f(x_val):
        return float(expr.subs(x, x_val).evalf())

    def df(x_val):
        return float(expr_prime.subs(x, x_val).evalf())
    try:
        root, iteration, history = newton_raphson(f, df, x0=float(x0), epsilon=float(eps))
    except ValueError as e:
        return (str(e), None, None)
    df_table = pd.DataFrame(history)
    return (root, iteration, df_table)
if __name__ == '__main__':
    f_example = lambda x: x ** 2 - 4
    df_example = lambda x: 2 * x
    root, n_iter, steps = newton_raphson(f=f_example, df=df_example, x0=1, epsilon=1e-06, max_iter=100)
    print(f'Root found: {root:.8f}  (after {n_iter} iteration(s))')
