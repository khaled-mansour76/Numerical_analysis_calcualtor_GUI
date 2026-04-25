import numpy as np
import pandas as pd
from itertools import permutations

def order(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    for p in permutations(range(n)):
        New_order_of_A = A[list(p)]
        New_order_of_b = b[list(p)]
        Bool = True
        for i in range(n):
            diag = abs(New_order_of_A[i, i])
            Sum = sum((abs(New_order_of_A[i, j]) for j in range(n) if i != j))
            if diag < Sum:
                Bool = False
                break
        if Bool:
            return (New_order_of_A, New_order_of_b)
    return (A, b)

def to_subscript(n):
    return str(n).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))

def jacobi(A, B, eps=1e-06):
    A, B = order(A, B)
    n = len(B)
    x = np.zeros(n)
    iteration = 0
    max_iter = 100
    history = []
    
    iter_dict = {'Iteration': 0}
    for i in range(n):
        # Store raw float; the GUI's precision formatter handles display.
        iter_dict[f'X{to_subscript(i + 1)}'] = x[i]
    history.append(iter_dict)
    
    while iteration < max_iter:
        iteration += 1
        old_x = x.copy()
        new_x = np.zeros(n)
        for i in range(n):
            sum_val = sum((A[i, j] * old_x[j] for j in range(n) if i != j))
            if A[i, i] == 0:
                raise ValueError("Zero pivot element encountered on diagonal.")
            new_x[i] = (B[i] - sum_val) / A[i, i]
        x = new_x
        
        iter_dict = {'Iteration': iteration}
        for i in range(n):
            iter_dict[f'X{to_subscript(i + 1)}'] = x[i]
        history.append(iter_dict)
        
        if np.allclose(x, old_x, atol=float(eps)):
            break
            
    column_names = ['Iteration'] + [f'X{to_subscript(i + 1)}' for i in range(n)]
    df = pd.DataFrame(history, columns=column_names)
    return (x, iteration, df)
