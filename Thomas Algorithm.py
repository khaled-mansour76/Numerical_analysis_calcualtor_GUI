import numpy as np

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



    digonal3 = np.diag(T , k=1)
    digonal2 = np.diag(T)
    digonal1 = np.diag(T , k= -1)

    y = np.zeros(4)
    z = np.zeros(4)
    x = np.zeros(4)
    for i in range(4) :
     if i ==  0 :
        y[i] = digonal2[i]
     else :
        y[i] = digonal2[i] - (digonal1[i-1] * digonal3[i-1]) / y[i-1]

    for i in range(4) :
       if i == 0 :
          z[i] = B[0] / digonal2[0]
       else :
          z[i] = (B[i] - digonal1[i-1] * z[i - 1])/ y[i]

    for i in range(3 , -1 , -1) :
       if i == 3 :
          x[i] = z[i]
       else :
          x[i] = z[i] - (digonal3[i ] * x[i+1] / y[i])
    print(f'y = \n{y} \n  z = \n {z} \n x = \n {x}')


a = [
    [1,4,0,0],
    [2,10,-4,0],
    [0,1,8,-1],
    [0,0,1,-6]
]
b = [10 , 7 , 6 , 4]
ThomasAlgorithm(a , b)
