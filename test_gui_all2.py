import tkinter as tk
from gui_module import NumericalMethodsGUI
from bisection_Method import Bisection
from secant import Secant
from gauss_Seidal import gauss_seidel

root = tk.Tk()
app = NumericalMethodsGUI(root)

try:
    res, iters, df = Bisection("x**2 - 4", 1, 3)
    app.plot_function("x**2 - 4", res, df)
    print("Bisection OK")
except Exception as e:
    print("Bisection Error:", e)

try:
    res, iters, df = Secant("x**2 - 4", 1, 3)
    app.plot_function("x**2 - 4", res, df)
    print("Secant OK")
except Exception as e:
    print("Secant Error:", e)

try:
    import numpy as np
    res, iters, df = gauss_seidel(np.array([[4,1],[1,3]]), np.array([1,2]))
    app.plot_matrix_convergence(df, "Gauss-Seidel", res)
    print("Gauss-Seidel OK")
except Exception as e:
    print("Gauss-Seidel Error:", e)

