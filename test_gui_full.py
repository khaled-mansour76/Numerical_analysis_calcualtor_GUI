import tkinter as tk
from gui_module import NumericalMethodsGUI

root = tk.Tk()
app = NumericalMethodsGUI(root)

# Test Newton
app.method_choice.set("Newton-Raphson")
app.setup_interface()
app.func_entry.insert(0, "x**2 - 4")
app.x0_entry.insert(0, "2.5")
app.eps_entry.delete(0, tk.END)
app.eps_entry.insert(0, "0.0001")
try:
    app.solve_roots()
    print("Newton GUI OK")
except Exception as e:
    print("Newton GUI Error:", e)

# Test Bisection
app.method_choice.set("Bisection")
app.setup_interface()
app.func_entry.insert(0, "x**2 - 4")
app.a_entry.insert(0, "1")
app.b_entry.insert(0, "3")
app.eps_entry.delete(0, tk.END)
app.eps_entry.insert(0, "0.0001")
try:
    app.solve_roots()
    print("Bisection GUI OK")
except Exception as e:
    print("Bisection GUI Error:", e)

