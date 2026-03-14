import numpy as np

def doolittle(A , B):
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

    v = np.zeros(n)
    for i in range(n):
        Rh = sum(L[i][m] * v[m] for m in range(i))
        v[i] = B[i] - Rh

    x = np.zeros(n)

    for i in range(n - 1, -1, -1):
        Rh = sum(U[i][m] * x[m] for m in range(i + 1, n))
        x[i] = (v[i] - Rh) / U[i][i]


    return L ,U , v ,x
    
