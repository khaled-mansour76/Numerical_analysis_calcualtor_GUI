import gui_module
import sys
import numpy as np
try:
    print("Testing Bisection Syntax Error...")
    print(gui_module.Bisection("x++2", 1, 3))
    print("Testing Bisection No Root...")
    print(gui_module.Bisection("x**2 + 4", 1, 3))
    print("Testing Doolittle Div by Zero Error...")
    A = np.array([[0, 1], [1, 1]], dtype=float)
    B = np.array([1, 2], dtype=float)
    print(gui_module.doolittle(A, B))
except Exception as e:
    import traceback
    traceback.print_exc()
