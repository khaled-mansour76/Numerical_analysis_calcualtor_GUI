import tkinter as tk
from gui_module import NumericalMethodsGUI
from newton_rapson import Newton_Raphson
from jacobis_Iteration_Method import jacobi
from thomas_Algorithm import ThomasAlgorithm
from false_position_method import False_Position

root = tk.Tk()
app = NumericalMethodsGUI(root)

# Test Bisection / False position plot
try:
    res, iters, df = False_Position("x**2 - 4", 1, 3)
    app.plot_function("x**2 - 4", res, df)
    print("plot_function OK")
except Exception as e:
    import traceback
    traceback.print_exc()

# Test Jacobi plot
try:
    res, iters, df = jacobi([[4,1],[1,3]], [1,2])
    app.plot_matrix_convergence(df, "Jacobi", res)
    print("Jacobi plot OK")
except Exception as e:
    import traceback
    traceback.print_exc()

# Test Thomas Algorithm plot
try:
    res, y, z, df = ThomasAlgorithm([[2,1,0],[1,2,1],[0,1,2]], [1,2,3])
    app.plot_matrix_convergence(df, "Thomas Algorithm", res)
    print("Thomas plot OK")
except Exception as e:
    import traceback
    traceback.print_exc()

