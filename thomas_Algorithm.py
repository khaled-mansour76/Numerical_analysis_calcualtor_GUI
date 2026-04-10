import numpy as np
import pandas as pd

def ThomasAlgorithm(T = [
    [1,4,0,0],
    [2,10,-4,0],
    [0,1,8,-1],
    [0,0,1,-6]
            ]  , B = [10 , 7 , 6 , 4]) :
    
    # digonal3 = [T[0][1] , T[1][2] , T[2][3]]
    # digonal2 = [T[0][0] , T[1][1] , T[2][2] , T[3][3]]
    # digonal1 = [T[1][0] , T[2][1] , T[3][2]]


    # dimintion = len(T)
    # digonal3 = [T[m][m+1] for m in range(dimintion-1)]  
    # digonal2 = [T[k][k] for k in range(dimintion)]
    # digonal1 = [T[i+1][i] for i in range(dimintion-1)]

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
            y[i] = digonal2[i] - (digonal1[i-1] * digonal3[i-1]) / y[i-1]

    for i in range(n):
        if i == 0:
            z[i] = B[0] / y[0]
        else:
            z[i] = (B[i] - digonal1[i-1] * z[i-1]) / y[i]

    for i in range(n - 1, -1, -1):
        if i == n - 1:
            x[i] = z[i]
        else:
            x[i] = z[i] - (digonal3[i] * x[i+1] / y[i])

    df_steps = pd.DataFrame({
        "Diagonal_Main": digonal2,
        "Intermediate_y": y,
        "Intermediate_z": z,
        "Final_Solution_x": x
    })

    return x, y, z, df_steps
