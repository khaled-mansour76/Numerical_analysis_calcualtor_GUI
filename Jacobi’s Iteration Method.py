import numpy as np
from itertools import permutations #we can use math,perm(n, r)
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
            Sum= sum(abs(New_order_of_A[i, j]) for j in range(n) if i != j)
            
            if diag < Sum:
                Bool = False
                break
        
        if Bool:
            return New_order_of_A, New_order_of_b
            
    return A, b

def jacobi(A, B):
    A, B = order(A, B)
    
    tempx, tempy, tempz = 0.0, 0.0, 0.0
    iteration = 0 
    epsilon = 0.00001
    max_iter = 11

    while iteration < max_iter:
        iteration += 1

        x_new = (B[0] - (A[0,1] * tempy) - (A[0,2] * tempz)) / A[0,0]
        y_new = (B[1] - (A[1,0] * tempx) - (A[1,2] * tempz)) / A[1,1]
        z_new = (B[2] - (A[2,0] * tempx) - (A[2,1] * tempy)) / A[2,2]

        if abs(x_new - tempx) < epsilon and abs(y_new - tempy) < epsilon and abs(z_new - tempz) < epsilon:
            return x_new, y_new, z_new, iteration
        
        tempx = x_new
        tempy = y_new
        tempz = z_new

    return tempx, tempy, tempz, iteration 


x , y , z , i  = jacobi([[1,2,1],[3,1,-1],[1,-1,4]],[0,0,3])
print(f'\n x = \n {x} \n y = \n {y} \n z = \n {z} \n i = \n {i}')
