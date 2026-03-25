import numpy as np
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
            Sum = sum(abs(New_order_of_A[i, j]) for j in range(n) if i != j)
            
            if diag < Sum:
                Bool = False
                break
        
        if Bool:
            return New_order_of_A, New_order_of_b
            
    return A, b

def gauss_seidel(A, B):
    A, B = order(A, B)
    
    x, y, z = 0.0, 0.0, 0.0
    iteration = 0 
    max_iter = 100

    while iteration < max_iter:
        iteration += 1
        
        old_x, old_y, old_z = x, y, z

        x = (B[0] - (A[0,1] * y) - (A[0,2] * z)) / A[0,0]
        
        y = (B[1] - (A[1,0] * x) - (A[1,2] * z)) / A[1,1]
        
        z = (B[2] - (A[2,0] * x) - (A[2,1] * y)) / A[2,2]

        if np.isclose(x, old_x, atol=1e-6) and \
           np.isclose(y, old_y, atol=1e-6) and \
           np.isclose(z, old_z, atol=1e-6):
            
            return x, y, z, iteration

    return x, y, z, iteration 

x, y, z, i = gauss_seidel([[1,-8,3], [8,2,-2],[2,1,9]], [-4,8,12])
print(f"--- Jacobi Result ---")
print(f"x = {x}")
print(f"y = {y}")
print(f"z = {z}")
print(f"iterations = {i}")