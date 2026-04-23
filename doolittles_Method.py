import numpy as np

def doolittle(A, B):
    A = np.array(A, dtype=float)
    B = np.array(B, dtype=float)
    n = len(A)
    L = np.zeros((n, n))
    U = np.zeros((n, n))
    for i in range(n):
        for k in range(i, n):
            sum_val = sum((L[i][j] * U[j][k] for j in range(i)))
            U[i][k] = A[i][k] - sum_val
        for k in range(i, n):
            if i == k:
                L[i][i] = 1
            else:
                sum_val = sum((L[k][j] * U[j][i] for j in range(i)))
                if U[i][i] == 0:
                    raise ValueError("Zero pivot encountered in Doolittle factorization.")
                L[k][i] = (A[k][i] - sum_val) / U[i][i]
    V = np.zeros(n)
    for i in range(n):
        sum_val = sum((L[i][j] * V[j] for j in range(i)))
        V[i] = B[i] - sum_val
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        sum_val = sum((U[i][j] * x[j] for j in range(i + 1, n)))
        if U[i][i] == 0:
            raise ValueError("Zero pivot encountered in Doolittle factorization.")
        x[i] = (V[i] - sum_val) / U[i][i]
    return (L, U, V, x)
