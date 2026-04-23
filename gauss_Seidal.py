import numpy as np
from itertools import permutations
import pandas as pd

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

def gauss_seidel(A, B, eps=1e-06):
    A, B = order(A, B)
    n = len(B)
    x = np.zeros(n)
    iteration = 0
    max_iter = 100
    history = []
    while iteration < max_iter:
        iteration += 1
        old_x = x.copy()
        for i in range(n):
            sum_val = 0
            for j in range(n):
                if i != j:
                    sum_val += A[i, j] * x[j]
            if A[i, i] == 0:
                raise ValueError("Zero pivot element encountered on diagonal.")
            x[i] = (B[i] - sum_val) / A[i, i]
        history.append(list(x))
        if np.allclose(x, old_x, atol=float(eps)):
            break
    column_names = [f'X{i + 1}' for i in range(n)]
    df = pd.DataFrame(history, columns=column_names)
    df.index.name = 'Iteration'
    df.index += 1
    return (x, iteration, df)
