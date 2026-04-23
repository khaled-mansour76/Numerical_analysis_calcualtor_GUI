import tkinter as tk
from gui_module import NumericalMethodsGUI
from newton_rapson import Newton_Raphson
from doolittles_Method import doolittle
import numpy as np

root = tk.Tk()
app = NumericalMethodsGUI(root)

# Test Newton
try:
    res, iters, df = Newton_Raphson("x**2 - 4", 2.5)
    app.plot_function("x**2 - 4", res, df)
    print("Newton OK")
except Exception as e:
    import traceback
    print("Newton Error:")
    traceback.print_exc()

# Test Doolittle
try:
    A = np.array([[2., 1., -1.], [-3., -1., 2.], [-2., 1., 2.]])
    B = np.array([8., -11., -3.])
    L, U, V, res = doolittle(A, B)
    import pandas as pd
    df = pd.DataFrame(res.reshape(-1, 1), columns=['Solution X'])
    app.plot_matrix_convergence(df, "Doolittle", res)
    print("Doolittle OK")
except Exception as e:
    import traceback
    print("Doolittle Error:")
    traceback.print_exc()

