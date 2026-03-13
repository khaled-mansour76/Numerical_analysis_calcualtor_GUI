import numpy as np

def doolittle(A):
    n = len(A)
    L = np.zeros((n, n))
    U = np.zeros((n, n))

    for i in range(n):
        for j in range(i, n):
            Rh = sum(L[i][m] * U[m][j] for m in range(i))
            U[i][j] = A[i][j] - Rh

        for k in range(i, n):
            if i == k:
                L[i][i] = 1 
            else:
                Rh = sum(L[k][m] * U[m][i] for m in range(i))
                L[k][i] = (A[k][i] - Rh) / U[i][i]

    

    





# A = np.array([[2, 1, 4],
#               [8, -3, 2],
#               [4, 11, -1]], dtype=float)

# L,U= doolittle(A)

# print("Lower Matrix (L):")
# print(L)

# print("\nUpper Matrix (U):")
# print(U)

# print(f"\n L * U = A \n {np.dot(L, U)}")
