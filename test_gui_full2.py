import tkinter as tk
from gui_module import NumericalMethodsGUI

root = tk.Tk()
app = NumericalMethodsGUI(root)

# Test Jacobi
app.method_choice.set("Jacobi")
app.setup_interface()
app.dim_entry.insert(0, "2")
app.generate_matrix_grid()
app.matrix_entries[0][0].insert(0, "4")
app.matrix_entries[0][1].insert(0, "1")
app.matrix_entries[1][0].insert(0, "1")
app.matrix_entries[1][1].insert(0, "3")
app.vector_entries[0].insert(0, "1")
app.vector_entries[1].insert(0, "2")
try:
    app.solve_system()
    print("Jacobi GUI OK")
except Exception as e:
    print("Jacobi GUI Error:", e)

# Test Gauss-Seidel
app.method_choice.set("Gauss-Seidel")
app.setup_interface()
app.dim_entry.insert(0, "2")
app.generate_matrix_grid()
app.matrix_entries[0][0].insert(0, "4")
app.matrix_entries[0][1].insert(0, "1")
app.matrix_entries[1][0].insert(0, "1")
app.matrix_entries[1][1].insert(0, "3")
app.vector_entries[0].insert(0, "1")
app.vector_entries[1].insert(0, "2")
try:
    app.solve_system()
    print("Gauss-Seidel GUI OK")
except Exception as e:
    print("Gauss-Seidel GUI Error:", e)

# Test Doolittle
app.method_choice.set("Doolittle")
app.setup_interface()
app.dim_entry.insert(0, "2")
app.generate_matrix_grid()
app.matrix_entries[0][0].insert(0, "1")
app.matrix_entries[0][1].insert(0, "2")
app.matrix_entries[1][0].insert(0, "3")
app.matrix_entries[1][1].insert(0, "4")
app.vector_entries[0].insert(0, "5")
app.vector_entries[1].insert(0, "6")
try:
    app.solve_system()
    print("Doolittle GUI OK")
except Exception as e:
    print("Doolittle GUI Error:", e)

