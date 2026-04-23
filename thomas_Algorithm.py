import numpy as np
import pandas as pd

def ThomasAlgorithm(T=[[1, 4, 0, 0], [2, 10, -4, 0], [0, 1, 8, -1], [0, 0, 1, -6]], B=[10, 7, 6, 4]):
    T = np.array(T, dtype=float)
    B = np.array(B, dtype=float)
    n = len(B)
    digonal3 = np.diag(T, k=1)
    digonal2 = np.diag(T)
    digonal1 = np.diag(T, k=-1)
    y = np.zeros(n)
    z = np.zeros(n)
    x = np.zeros(n)
    for i in range(n):
        if i == 0:
            y[i] = digonal2[i]
        else:
            if y[i - 1] == 0:
                raise ValueError("Zero pivot encountered in Thomas Algorithm.")
            y[i] = digonal2[i] - digonal1[i - 1] * digonal3[i - 1] / y[i - 1]
    for i in range(n):
        if i == 0:
            if y[0] == 0:
                raise ValueError("Zero pivot encountered in Thomas Algorithm.")
            z[i] = B[0] / y[0]
        else:
            if y[i] == 0:
                raise ValueError("Zero pivot encountered in Thomas Algorithm.")
            z[i] = (B[i] - digonal1[i - 1] * z[i - 1]) / y[i]
    for i in range(n - 1, -1, -1):
        if i == n - 1:
            x[i] = z[i]
        else:
            if y[i] == 0:
                raise ValueError("Zero pivot encountered in Thomas Algorithm.")
            x[i] = z[i] - digonal3[i] * x[i + 1] / y[i]
    df_steps = pd.DataFrame({'Diagonal_Main': digonal2, 'Intermediate_y': y, 'Intermediate_z': z, 'Final_Solution_x': x})
    return (x, y, z, df_steps)
