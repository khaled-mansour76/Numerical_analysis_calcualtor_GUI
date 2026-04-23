import gui_module
import sys
import numpy as np
try:
    print("Testing Bisection...")
    print(gui_module.Bisection("x**2 - 4", 1, 3))
    print("Testing False Position...")
    print(gui_module.False_Position("x**2 - 4", 1, 3))
    print("Testing Newton Raphson...")
    print(gui_module.Newton_Raphson("x**2 - 4", 3))
    print("Testing Secant...")
    print(gui_module.Secant("x**2 - 4", 1, 3))
    print("Testing Doolittle...")
    A = np.array([[2, -1, 1], [3, 3, 9], [3, 3, 5]], dtype=float)
    B = np.array([-1, 0, 4], dtype=float)
    print(gui_module.doolittle(A, B))
    print("Testing Gauss Seidel...")
    A_dom = np.array([[4, 1, 1], [1, 5, 2], [1, 1, 3]], dtype=float)
    B_dom = np.array([6, 8, 5], dtype=float)
    print(gui_module.gauss_seidel(A_dom, B_dom))
    print("Testing Jacobi...")
    print(gui_module.jacobi(A_dom, B_dom))
    print("Testing Thomas...")
    A_td = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 2]], dtype=float)
    B_td = np.array([1, 0, 1], dtype=float)
    print(gui_module.ThomasAlgorithm(A_td, B_td))
    print("All tests finished.")
except Exception as e:
    import traceback
    traceback.print_exc()
