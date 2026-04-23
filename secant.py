import math
import pandas as pd
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

def secant(f, x0, x1, epsilon=1e-06, max_iter=100):
    xn_1 = float(x0)
    xn = float(x1)
    history = []
    for iteration in range(1, max_iter + 1):
        fxn_1 = f(xn_1)
        fxn = f(xn)
        denom = fxn - fxn_1
        if denom == 0:
            raise ValueError(f'f(x_n) == f(x_n-1) at iteration {iteration}. Secant method cannot continue (division by zero).')
        xn1 = xn - fxn * (xn - xn_1) / denom
        fxn1 = f(xn1)
        history.append({'Iteration': iteration, 'xn-1': xn_1, 'xn': xn, 'f(xn-1)': fxn_1, 'f(xn)': fxn, 'xn+1': xn1, 'f(xn+1)': fxn1})
        if abs(xn1 - xn) < epsilon or abs(fxn1) < epsilon:
            return (xn1, iteration, history)
        xn_1 = xn
        xn = xn1
    return (xn, max_iter, history)

def Secant(func, x0, x1, eps=1e-06):
    x = sp.symbols('x')
    local_dict = {'pi': sp.pi, 'e': sp.E, 'exp': sp.exp, 'cos': sp.cos, 'sin': sp.sin, 'tan': sp.tan}
    transformations = standard_transformations + (implicit_multiplication_application,)
    try:
        expr = parse_expr(func, local_dict=local_dict, transformations=transformations)
    except Exception as e:
        return (f'Check syntax: {str(e)}', None, None)

    def f(x_val):
        return float(expr.subs(x, x_val).evalf())
    try:
        root, iteration, history = secant(f, x0=float(x0), x1=float(x1), epsilon=float(eps))
    except ValueError as e:
        return (str(e), None, None)
    df_table = pd.DataFrame(history)
    return (root, iteration, df_table)
if __name__ == '__main__':
    f_example = lambda x: x ** 2 - 4
    root, n_iter, steps = secant(f=f_example, x0=1, x1=3, epsilon=1e-06, max_iter=100)
    print(f'Root found: {root:.8f}  (after {n_iter} iteration(s))')
