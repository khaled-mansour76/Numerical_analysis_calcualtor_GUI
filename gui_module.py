import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
import sys

HAS_MATPLOTLIB = False
try:
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import sympy as sp
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    HAS_MATPLOTLIB = True
except ImportError:
    pass

try:
    from bisection_Method import Bisection
    from false_position_method import False_Position
    from newton_rapson import Newton_Raphson
    from secant import Secant
    from doolittles_Method import doolittle
    from gauss_Seidal import gauss_seidel
    from jacobis_Iteration_Method import jacobi
    from thomas_Algorithm import ThomasAlgorithm
except ImportError as e:
    import tkinter.messagebox as mb
    root = tk.Tk()
    root.withdraw()
    mb.showerror('Dependencies Error', f'Failed to load dependencies: {e}\n\nPlease ensure you run the script within your virtual environment (e.g. ./bin/python3 main.py) or install the required packages (numpy, pandas, sympy).')
    sys.exit(1)

class NumericalMethodsGUI:

    def __init__(self, root):
        self.root = root
        self.root.title('Advanced Numerical Analysis Solver')
        self.root.geometry('1000x850')
        self.root.configure(bg='#f5f6f7')
        header_frame = tk.Frame(root, bg='#2c3e50')
        header_frame.pack(fill='x')
        header = tk.Label(header_frame, text='Numerical Methods Solver', font=('Segoe UI', 22, 'bold'), fg='white', bg='#2c3e50')
        header.pack(pady=20)
        selection_container = tk.Frame(root, bg='#f5f6f7')
        selection_container.pack(pady=20)
        tk.Label(selection_container, text='Select Calculation Method:', font=('Segoe UI', 12), bg='#f5f6f7').pack()
        self.method_choice = ttk.Combobox(selection_container, values=['Bisection', 'False Position', 'Newton-Raphson', 'Secant', 'Doolittle', 'Gauss-Seidel', 'Jacobi', 'Thomas Algorithm'], state='readonly', width=35, font=('Segoe UI', 11))
        self.method_choice.pack(pady=10)
        self.method_choice.bind('<<ComboboxSelected>>', self.setup_interface)
        self.content_frame = tk.Frame(root, bg='white', bd=1, relief='groove')
        self.content_frame.pack(fill='both', expand=True, padx=40, pady=10)
        self.input_frame = tk.Frame(self.content_frame, bg='white')
        self.input_frame.pack(side='left', fill='both', expand=True)
        self.plot_frame = tk.Frame(self.content_frame, bg='#f9f9f9', bd=1, relief='sunken', width=400)
        self.plot_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        self.result_banner = tk.Frame(root, bg='#ecf0f1')
        self.result_banner.pack(fill='x', side='bottom')
        self.result_label = tk.Label(self.result_banner, text='Ready', font=('Segoe UI', 13, 'bold'), fg='#2980b9', bg='#ecf0f1')
        self.result_label.pack(pady=15)

    def setup_interface(self, event=None):
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        self.result_label.config(text='Ready', fg='#2980b9')
        method = self.method_choice.get()
        if not method:
            return
        if method in ['Bisection', 'False Position', 'Newton-Raphson', 'Secant']:
            self.setup_roots_interface()
        else:
            self.setup_matrix_interface()

    def setup_roots_interface(self):
        method = self.method_choice.get()
        container = tk.Frame(self.input_frame, bg='white')
        container.pack(pady=40)
        tk.Label(container, text='Function f(x):', font=('Segoe UI', 12, 'bold'), bg='white').pack(anchor='w')
        self.func_entry = tk.Entry(container, width=60, font=('Consolas', 14), bd=2, relief='ridge')
        self.func_entry.pack(pady=10)
        inputs_frame = tk.Frame(container, bg='white')
        inputs_frame.pack(pady=20)
        if method == 'Newton-Raphson':
            tk.Label(inputs_frame, text='Initial Guess (x0):', font=('Segoe UI', 11), bg='white').grid(row=0, column=0, padx=10)
            self.x0_entry = tk.Entry(inputs_frame, width=15, font=('Consolas', 13), bd=2)
            self.x0_entry.grid(row=0, column=1, padx=10)
        elif method == 'Secant':
            tk.Label(inputs_frame, text='First Guess (x0):', font=('Segoe UI', 11), bg='white').grid(row=0, column=0, padx=10)
            self.x0_entry = tk.Entry(inputs_frame, width=15, font=('Consolas', 13), bd=2)
            self.x0_entry.grid(row=0, column=1, padx=10)
            tk.Label(inputs_frame, text='Second Guess (x1):', font=('Segoe UI', 11), bg='white').grid(row=0, column=2, padx=10)
            self.x1_entry = tk.Entry(inputs_frame, width=15, font=('Consolas', 13), bd=2)
            self.x1_entry.grid(row=0, column=3, padx=10)
        else:
            tk.Label(inputs_frame, text='Start Point (a):', font=('Segoe UI', 11), bg='white').grid(row=0, column=0, padx=10)
            self.a_entry = tk.Entry(inputs_frame, width=15, font=('Consolas', 13), bd=2)
            self.a_entry.grid(row=0, column=1, padx=10)
            tk.Label(inputs_frame, text='End Point (b):', font=('Segoe UI', 11), bg='white').grid(row=0, column=2, padx=10)
            self.b_entry = tk.Entry(inputs_frame, width=15, font=('Consolas', 13), bd=2)
            self.b_entry.grid(row=0, column=3, padx=10)
            
        tk.Label(inputs_frame, text='Epsilon (Error rate):', font=('Segoe UI', 11), bg='white').grid(row=1, column=0, padx=10, pady=15)
        self.eps_entry = tk.Entry(inputs_frame, width=15, font=('Consolas', 13), bd=2)
        self.eps_entry.insert(0, '0.0001')
        self.eps_entry.grid(row=1, column=1, padx=10, pady=15)
        
        buttons_frame = tk.Frame(container, bg='white')
        buttons_frame.pack(pady=30)
        tk.Button(buttons_frame, text='RUN ANALYSIS', command=self.solve_roots, bg='#27ae60', fg='white', font=('Segoe UI', 12, 'bold'), width=20, height=2, cursor='hand2').grid(row=0, column=0, padx=10)
        tk.Button(buttons_frame, text='RESET', command=self.setup_interface, bg='#e74c3c', fg='white', font=('Segoe UI', 12, 'bold'), width=20, height=2, cursor='hand2').grid(row=0, column=1, padx=10)

    def setup_matrix_interface(self):
        dim_frame = tk.Frame(self.input_frame, bg='white')
        dim_frame.pack(pady=30)
        tk.Label(dim_frame, text='Enter Matrix Size (n):', font=('Segoe UI', 12, 'bold'), bg='white').pack(side='left', padx=10)
        self.dim_entry = tk.Entry(dim_frame, width=10, font=('Consolas', 13), bd=2)
        self.dim_entry.pack(side='left', padx=10)
        tk.Button(dim_frame, text='GENERATE GRID', command=self.generate_matrix_grid, bg='#2980b9', fg='white', font=('Segoe UI', 10, 'bold'), padx=15).pack(side='left', padx=10)
        tk.Button(dim_frame, text='RESET', command=self.setup_interface, bg='#e74c3c', fg='white', font=('Segoe UI', 10, 'bold'), padx=15).pack(side='left', padx=10)
        self.grid_container = tk.Frame(self.input_frame, bg='white')
        self.grid_container.pack(pady=20)

    def generate_matrix_grid(self):
        for widget in self.grid_container.winfo_children():
            widget.destroy()
        try:
            val = self.dim_entry.get()
            if not val:
                return
            n = int(val)
            if n > 10:
                raise ValueError('Size too large for display')
            self.matrix_entries = []
            self.vector_entries = []
            for j in range(n):
                tk.Label(self.grid_container, text=f'Col {j + 1}', font=('Segoe UI', 9, 'bold'), bg='white').grid(row=0, column=j)
            tk.Label(self.grid_container, text=' | Result (B)', font=('Segoe UI', 9, 'bold'), fg='red', bg='white').grid(row=0, column=n)
            for i in range(n):
                row_entries = []
                for j in range(n):
                    e = tk.Entry(self.grid_container, width=10, font=('Consolas', 12), justify='center', bd=2)
                    e.grid(row=i + 1, column=j, padx=4, pady=4)
                    e.bind('<KeyRelease>', self.check_matrix_properties)
                    row_entries.append(e)
                self.matrix_entries.append(row_entries)
                be = tk.Entry(self.grid_container, width=10, font=('Consolas', 12, 'bold'), fg='red', justify='center', bd=2, bg='#fff5f5')
                be.grid(row=i + 1, column=n, padx=15, pady=4)
                self.vector_entries.append(be)
                
            if self.method_choice.get() in ['Jacobi', 'Gauss-Seidel']:
                eps_frame = tk.Frame(self.grid_container, bg='white')
                eps_frame.grid(row=n+2, column=0, columnspan=n+1, pady=15)
                tk.Label(eps_frame, text='Error Rate (Epsilon):', font=('Segoe UI', 11, 'bold'), bg='white').pack(side='left', padx=5)
                self.eps_matrix_entry = tk.Entry(eps_frame, width=15, font=('Consolas', 12), bd=2)
                self.eps_matrix_entry.insert(0, '0.0001')
                self.eps_matrix_entry.pack(side='left')

            tk.Button(self.grid_container, text='SOLVE SYSTEM', command=self.solve_system, bg='#27ae60', fg='white', font=('Segoe UI', 12, 'bold'), width=30, height=2, cursor='hand2').grid(row=n+3, column=0, columnspan=n+1, pady=20)
        except ValueError as e:
            messagebox.showerror('Error', str(e))

    def solve_roots(self):
        method = self.method_choice.get()
        try:
            f = self.func_entry.get()
            eps = float(self.eps_entry.get())
            if method == 'Newton-Raphson':
                x0 = float(self.x0_entry.get())
                res, iters, df = Newton_Raphson(f, x0, eps)
            elif method == 'Secant':
                x0 = float(self.x0_entry.get())
                x1 = float(self.x1_entry.get())
                res, iters, df = Secant(f, x0, x1, eps)
            elif method == 'Bisection':
                a = float(self.a_entry.get())
                b = float(self.b_entry.get())
                res, iters, df = Bisection(f, a, b, eps)
            elif method == 'False Position':
                a = float(self.a_entry.get())
                b = float(self.b_entry.get())
                res, iters, df = False_Position(f, a, b, eps)
                
            if isinstance(res, str):
                raise ValueError(res)
                
            self.result_label.config(text=f'SUCCESS: Root found at {res:.6f} in {iters} iterations', fg='#27ae60')
            self.display_steps(df, method)
            self.plot_function(f, res, df)
        except Exception as e:
            messagebox.showerror('Math Error', str(e))

    def solve_system(self):
        method = self.method_choice.get()
        try:
            n = len(self.matrix_entries)
            A = [[float(self.matrix_entries[i][j].get()) for j in range(n)] for i in range(n)]
            B = [float(self.vector_entries[i].get()) for i in range(n)]
            A_np = np.array(A)
            B_np = np.array(B)
            if method == 'Jacobi':
                eps = float(self.eps_matrix_entry.get())
                res, iters, df = jacobi(A_np, B_np, eps)
            elif method == 'Gauss-Seidel':
                eps = float(self.eps_matrix_entry.get())
                res, iters, df = gauss_seidel(A_np, B_np, eps)
            elif method == 'Thomas Algorithm':
                res, y, z, df = ThomasAlgorithm(A_np, B_np)
            elif method == 'Doolittle':
                L, U, V, res = doolittle(A_np, B_np)
                df = pd.DataFrame(res.reshape(-1, 1), columns=['Solution X'])
            self.result_label.config(text=f'SYSTEM SOLVED: Check the steps table for details', fg='#27ae60')
            self.display_steps(df, method)
            self.plot_matrix_convergence(df, method, res)
        except Exception as e:
            messagebox.showerror('Input Error', f'Check inputs: {str(e)}')

    def display_steps(self, df, method):
        if df is None:
            return
        table_win = tk.Toplevel(self.root)
        table_win.title('Step-by-Step Numerical Analysis')
        table_win.geometry('800x500')
        style = ttk.Style()
        style.configure('Treeview', font=('Segoe UI', 10), rowheight=25)
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
        tree = ttk.Treeview(table_win, style='Treeview')
        tree['columns'] = list(df.columns)
        tree['show'] = 'headings'
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor='center')
        for (_, row) in df.iterrows():
            formatted_row = [(f'{val:.6f}' if isinstance(val, (float, np.float64)) else val) for val in row]
            tree.insert('', 'end', values=formatted_row)
        vsb = ttk.Scrollbar(table_win, orient='vertical', command=tree.yview)
        hsb = ttk.Scrollbar(table_win, orient='horizontal', command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.pack(expand=True, fill='both')
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        
        btn_frame = tk.Frame(table_win)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="View Steps Explanation", command=lambda: self.explain_steps(df, method), bg='#8e44ad', fg='white', font=('Segoe UI', 11, 'bold'), cursor='hand2').pack()

    def check_matrix_properties(self, event=None):
        if not hasattr(self, 'suggest_label'):
            self.suggest_label = tk.Label(self.grid_container, text="", font=('Segoe UI', 11, 'bold'), fg='#d35400', bg='white')
            # Place label below epsilon but above solve button
            n = len(self.matrix_entries)
            self.suggest_label.grid(row=n+4, column=0, columnspan=n+1, pady=5)
            
        try:
            n = len(self.matrix_entries)
            A = np.zeros((n, n))
            for i in range(n):
                for j in range(n):
                    val = self.matrix_entries[i][j].get()
                    if not val:
                        self.suggest_label.config(text="")
                        return
                    A[i, j] = float(val)
                    
            # Check Tridiagonal
            is_tridiag = True
            for i in range(n):
                for j in range(n):
                    if abs(i - j) > 1 and A[i, j] != 0:
                        is_tridiag = False
                        break
            
            # Additional check to ensure tridiagonal elements aren't all exactly zero (which would be trivial/diagonal)
            if is_tridiag and n > 1:
                super_diag_nonzero = any(abs(A[i, i+1]) > 0 for i in range(n-1))
                sub_diag_nonzero = any(abs(A[i+1, i]) > 0 for i in range(n-1))
                if super_diag_nonzero or sub_diag_nonzero:
                    self.suggest_label.config(text="✨ Suggested Method: Thomas Algorithm (Tridiagonal Detected) ✨")
                    return
                    
            # Check Diagonal Dominance
            is_diag_dom = True
            for i in range(n):
                diag = abs(A[i, i])
                sum_others = sum(abs(A[i, j]) for j in range(n) if i != j)
                if diag <= sum_others:
                    is_diag_dom = False
                    break
            
            if is_diag_dom:
                self.suggest_label.config(text="✨ Suggested Method: Gauss-Seidel or Jacobi (Diagonally Dominant) ✨")
                return
                
            self.suggest_label.config(text="")
        except ValueError:
            self.suggest_label.config(text="")

    def explain_steps(self, df, method):
        explain_win = tk.Toplevel(self.root)
        explain_win.title(f"Step Explanations - {method}")
        explain_win.geometry('700x500')
        
        text_widget = tk.Text(explain_win, font=('Segoe UI', 11), wrap='word', bg='#fefefe', padx=15, pady=15)
        text_widget.pack(expand=True, fill='both')
        
        explanations = []
        if method == "Bisection":
            for _, row in df.iterrows():
                explanations.append(f"Iteration {int(row['Iteration'])}: Evaluated midpoint c = {row['c (Midpoint)']:.6f}. The function value f(c) = {row['f(c)']:.6f}. The bounds were updated from [a={row['a']:.4f}, b={row['b']:.4f}] to narrow the search bracket.")
        elif method == "Newton-Raphson":
             for _, row in df.iterrows():
                deriv = row.get("f'(xn)", 0)
                explanations.append(f"Iteration {int(row['Iteration'])}: Starting at xn = {row['xn']:.6f}, evaluated f(xn) = {row['f(xn)']:.6f} and derivative f'(xn) = {deriv:.6f}. Calculated next approximation.")
        elif method == "Secant":
             for _, row in df.iterrows():
                explanations.append(f"Iteration {int(row['Iteration'])}: Used points x_n-1 = {row['x_n-1']:.6f} and x_n = {row['x_n']:.6f} to draw secant line. Next approximation is x_n+1 = {row['x_n+1']:.6f}.")
        elif method == "False Position":
             for _, row in df.iterrows():
                explanations.append(f"Iteration {int(row['Iteration'])}: Calculated point of intersection with x-axis xs = {row['xs']:.6f}. Evaluated f(xs) = {row['f(xs)']:.6f}. Updated brackets [a={row['a']:.4f}, b={row['b']:.4f}].")
        elif method in ["Jacobi", "Gauss-Seidel"]:
             for idx, row in df.iterrows():
                explanations.append(f"Iteration {idx}: Updated variables closer to exact solution. " + ", ".join([f"{col} = {row[col]:.5f}" for col in df.columns]))
        elif method == "Thomas Algorithm":
             explanations.append("Thomas Algorithm is an exact method (no iterations). It executes in three steps:")
             explanations.append("1. Forward Sweep to eliminate lower diagonal (Intermediate y).")
             explanations.append("2. Process the B array (Intermediate z).")
             explanations.append("3. Back Substitution to find Final Solution x.")
        elif method == "Doolittle":
             explanations.append("Doolittle factorization splits the matrix into Lower (L) and Upper (U) triangular matrices.")
             explanations.append("Then solves Ly = B, and finally Ux = y to obtain the result.")
        
        for p in explanations:
            text_widget.insert(tk.END, p + "\n\n")
            
        text_widget.config(state='disabled')

    def plot_function(self, func_str, root_val, df):
        if not HAS_MATPLOTLIB:
            return
            
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
            
        try:
            x = sp.symbols('x')
            local_dict = {'pi': sp.pi, 'e': sp.E, 'exp': sp.exp, 'cos': sp.cos, 'sin': sp.sin, 'tan': sp.tan}
            transformations = standard_transformations + (implicit_multiplication_application,)
            expr = parse_expr(func_str, local_dict=local_dict, transformations=transformations)
            f_lamb = sp.lambdify(x, expr, "numpy")
            
            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)
            
            # Determine range based on steps if available
            x_vals = []
            if 'a' in df.columns and 'b' in df.columns:
                x_vals.extend(df['a'].tolist())
                x_vals.extend(df['b'].tolist())
            elif 'xn' in df.columns:
                x_vals.extend(df['xn'].tolist())
            elif 'x_n' in df.columns:
                x_vals.extend(df['x_n'].tolist())
                
            if x_vals:
                min_x, max_x = min(x_vals) - 1, max(x_vals) + 1
            else:
                min_x, max_x = root_val - 5, root_val + 5
                
            X_plot = np.linspace(min_x, max_x, 400)
            Y_plot = f_lamb(X_plot)
            
            ax.plot(X_plot, Y_plot, label='f(x)', color='#2980b9')
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(X_plot[0], color='black', linewidth=1)
            
            # Highlight root
            ax.plot(root_val, 0, 'go', markersize=8, label='Root')
            
            ax.set_title("Function Plot & Root")
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.6)
            
            canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            tk.Label(self.plot_frame, text=f"Could not render plot:\n{str(e)}").pack()

    def plot_matrix_convergence(self, df, method, final_res):
        if not HAS_MATPLOTLIB:
            return
            
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
            
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        if method in ['Jacobi', 'Gauss-Seidel']:
            for col in df.columns:
                ax.plot(df.index, df[col], marker='o', label=col)
            
            ax.set_title(f"Convergence of {method}")
            ax.set_xlabel("Iteration")
            ax.set_ylabel("Value")
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.6)
        else:
            # Exact methods: Plot the final vector values
            x_pos = np.arange(len(final_res))
            # Handle Thomas Algorithm which returns tuple (x,y,z,df)
            res_vector = final_res[0] if isinstance(final_res, tuple) else final_res
            ax.bar(x_pos, res_vector, align='center', alpha=0.7, color='#27ae60')
            ax.set_xticks(x_pos)
            ax.set_xticklabels([f"X{i+1}" for i in range(len(res_vector))])
            ax.set_title("Final Solution Vector")
            ax.set_ylabel("Value")
            ax.grid(True, axis='y', linestyle='--', alpha=0.6)
            
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
