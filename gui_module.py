import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
import sys
import datetime

# ── Module-level helper ────────────────────────────────────────────────────────
def to_subscript(n):
    """Convert a digit string to its Unicode subscript equivalent (e.g. 1 → ₁)."""
    return str(n).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))


# ── Optional dependencies ──────────────────────────────────────────────────────
HAS_MATPLOTLIB = False
try:
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import sympy as sp
    from sympy.parsing.sympy_parser import (
        parse_expr, standard_transformations,
        implicit_multiplication_application, convert_xor
    )
    HAS_MATPLOTLIB = True
except ImportError:
    pass

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# ── Method imports ─────────────────────────────────────────────────────────────
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
    mb.showerror(
        'Dependencies Error',
        f'Failed to load dependencies: {e}\n\n'
        'Please ensure you run the script within your virtual environment '
        '(e.g. ./bin/python3 main.py) or install the required packages '
        '(numpy, pandas, sympy).'
    )
    sys.exit(1)

# ── Interpolation method imports (added) ──────────────────────────────────────
try:
    import newton_forward
    import newton_backward
    import stirling
    import lagrange
    import lagrange_inverse
    HAS_INTERP = True
except ImportError:
    HAS_INTERP = False

_INTERP_METHODS = [
    'Newton Forward',
    'Newton Backward',
    'Stirling',
    'Lagrange',
    'Lagrange Inverse',
]


# ══════════════════════════════════════════════════════════════════════════════
class NumericalMethodsGUI:
    """
    Main GUI controller for the Advanced Numerical Analysis Solver.

    New features added (2026-04):
      1. Precision Control  — choose Decimal Places or Significant Figures
                              with a live preview; every numeric output uses
                              self.fmt() so a single change propagates everywhere.
      2. Keyboard Navigation — Enter advances through fields then solves;
                              Escape closes step windows or resets the form;
                              Tab order is wired throughout the matrix grid.
      3. Auto-fill Zeros    — "Fill Empty Cells with Zeros" button fills only
                              blank matrix / B-vector cells (with a green flash).
    """

    # ── Construction ──────────────────────────────────────────────────────────

    def __init__(self, root):
        self.root = root
        self.root.title('Advanced Numerical Analysis Solver')
        self.root.geometry('1050x900')

        # ── Precision state ────────────────────────────────────────────────
        # StringVars decouple values from widget lifecycle: they survive
        # setup_interface() teardown, so precision is never accidentally reset.
        self.precision_mode_var   = tk.StringVar(value="Decimal Places")
        self.precision_digits_var = tk.StringVar(value="6")

        # ── Background image ───────────────────────────────────────────────
        self.bg_photo = None
        if HAS_PIL:
            try:
                self.original_bg_image = Image.open("background.jpeg")
                self.bg_photo = ImageTk.PhotoImage(
                    self.original_bg_image.resize((1050, 900), Image.LANCZOS)
                )
                self.bg_label = tk.Label(root, image=self.bg_photo)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                self.root.bind('<Configure>', self.resize_bg)
            except Exception:
                pass
        else:
            self.root.configure(bg='#1c1c2e')

        # ── Header ────────────────────────────────────────────────────────
        header_frame = tk.Frame(root, bg='#0f111a', bd=2, relief='ridge')
        header_frame.pack(fill='x')
        tk.Label(
            header_frame,
            text='Numerical Methods Solver',
            font=('Courier New', 22, 'bold'),
            fg='#00ffcc', bg='#0f111a'
        ).pack(pady=15)

        # ── Method selector ────────────────────────────────────────────────
        selection_container = tk.Frame(root, bg='#0f111a')
        selection_container.pack(pady=10)
        tk.Label(
            selection_container,
            text='Select Calculation Method:',
            font=('Courier New', 12, 'bold'),
            fg='#00ffcc', bg='#0f111a'
        ).pack()
        self.method_choice = ttk.Combobox(
            selection_container,
            values=[
                'Bisection', 'False Position', 'Newton-Raphson', 'Secant',
                'Doolittle', 'Gauss-Seidel', 'Jacobi', 'Thomas Algorithm',
                '── Interpolation Methods ──',
                'Newton Forward', 'Newton Backward', 'Stirling',
                'Lagrange', 'Lagrange Inverse',
            ],
            state='readonly', width=35, font=('Segoe UI', 11)
        )
        self.method_choice.pack(pady=5)
        self.method_choice.bind('<<ComboboxSelected>>', self.setup_interface)

        # ── Precision Control Panel ────────────────────────────────────────
        # Sits between the method selector and the main content area.
        # Always visible and unaffected by method switches (StringVars persist).
        precision_panel = tk.Frame(root, bg='#0f111a', pady=6)
        precision_panel.pack(fill='x', padx=40)

        tk.Label(
            precision_panel, text='Precision:',
            font=('Courier New', 10, 'bold'), fg='#00ffcc', bg='#0f111a'
        ).pack(side='left', padx=(0, 6))

        self.precision_combo = ttk.Combobox(
            precision_panel,
            textvariable=self.precision_mode_var,
            values=["Decimal Places", "Significant Figures"],
            state='readonly', width=18, font=('Segoe UI', 10)
        )
        self.precision_combo.pack(side='left', padx=4)

        tk.Label(
            precision_panel, text='Digits:',
            font=('Courier New', 10, 'bold'), fg='#00ffcc', bg='#0f111a'
        ).pack(side='left', padx=(10, 4))

        tk.Entry(
            precision_panel,
            textvariable=self.precision_digits_var,
            width=4, font=('Consolas', 12),
            bg='#1c1c2e', fg='#00ffcc',
            insertbackground='#00ffcc', bd=2
        ).pack(side='left', padx=4)

        # Live preview: updates automatically when mode or digits changes
        self.precision_preview_lbl = tk.Label(
            precision_panel, text='',
            font=('Courier New', 10), fg='#7f8c8d', bg='#0f111a'
        )
        self.precision_preview_lbl.pack(side='left', padx=(14, 0))

        # Trace StringVars; the callbacks receive (name, index, operation)
        self.precision_mode_var.trace_add('write', self._update_precision_preview)
        self.precision_digits_var.trace_add('write', self._update_precision_preview)
        self._update_precision_preview()   # initial render

        # ── Content area ───────────────────────────────────────────────────
        self.content_frame = tk.Frame(root, bg='#1c1c2e', bd=1, relief='groove')
        self.content_frame.pack(fill='both', expand=True, padx=40, pady=10)

        self.input_frame = tk.Frame(self.content_frame, bg='#1c1c2e')
        self.input_frame.pack(side='left', fill='both', expand=True)

        self.plot_frame = tk.Frame(
            self.content_frame, bg='#0f111a', bd=1, relief='sunken', width=400
        )
        self.plot_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        # ── Result banner ──────────────────────────────────────────────────
        self.result_banner = tk.Frame(
            root, bg='black', highlightbackground='gray',
            highlightthickness=1, bd=0
        )
        self.result_banner.pack(fill='x', side='bottom', padx=40, pady=20)
        tk.Label(
            self.result_banner, text='Root',
            font=('Courier New', 14, 'bold'),
            fg='black', bg='yellow', padx=10
        ).pack(anchor='w', padx=5, pady=5)
        self.result_container = tk.Frame(self.result_banner, bg='black')
        self.result_container.pack(fill='both', expand=True, pady=10)
        self.result_label = tk.Label(
            self.result_container, text='Ready',
            font=('Courier New', 48, 'bold'),
            fg='yellow', bg='black', justify='center', anchor='center'
        )
        self.result_label.pack(expand=True, pady=10)

        # ── Root-level keyboard shortcuts ──────────────────────────────────
        # <Return>  → _smart_solve  (routes to the active method's solver)
        # <Escape>  → _on_escape    (closes a Toplevel, or resets the form)
        #
        # Note: individual Entry widgets bind <Return> to advance focus and
        # return "break" to prevent this root binding from also firing.
        self.root.bind('<Return>', lambda e: self._smart_solve())
        self.root.bind('<Escape>', self._on_escape)

    # ── Precision Helpers ──────────────────────────────────────────────────────

    @staticmethod
    def precision_format(value, mode, digits):
        """
        Format *value* (numeric) as a string according to *mode* and *digits*.

        mode  : "Decimal Places" | "Significant Figures"
        digits: positive integer, clamped to [1, 15] before calling

        Handles edge cases:
          • value == 0 with Significant Figures → "0.000…" (digits-1 zeros)
          • Non-finite floats (inf, nan)        → str() fallback
          • Any unexpected exception            → str(value) (never raises)

        Uses Python's built-in 'g' format for significant figures, which
        applies IEEE-754 rounding and strips superfluous trailing zeros.
        """
        try:
            v = float(value)
            if mode == "Significant Figures":
                if v == 0:
                    # e.g. 4 sig figs → "0.000"
                    return "0." + "0" * max(digits - 1, 0)
                # Python's :.{n}g format implements correct sig-fig rounding
                return f"{v:.{digits}g}"
            else:
                # Standard fixed decimal places
                return f"{v:.{digits}f}"
        except (ValueError, OverflowError, TypeError):
            return str(value)   # fallback — must never crash

    def _get_precision(self):
        """
        Read the current precision settings from the StringVars.
        Returns (mode: str, digits: int) with digits clamped to [1, 15].
        Falls back to ("Decimal Places", 6) if the digits field is invalid.
        """
        mode = self.precision_mode_var.get() or "Decimal Places"
        try:
            d = int(self.precision_digits_var.get())
            d = max(1, min(15, d))   # IEEE-754 double ≈ 15 significant digits
        except ValueError:
            d = 6                    # silent fallback
        return mode, d

    def fmt(self, value):
        """Shortcut: format *value* using the current precision settings."""
        mode, digits = self._get_precision()
        return self.precision_format(value, mode, digits)

    def _update_precision_preview(self, *_):
        """
        Refresh the live preview label next to the precision controls.
        Called automatically by StringVar traces whenever mode or digits changes.
        Uses π as a recognisable sample value.
        """
        try:
            preview = self.fmt(3.14159265358979)
            self.precision_preview_lbl.config(text=f"  e.g.  π ≈ {preview}")
        except Exception:
            pass   # widget may not exist yet on very first trace fire

    # ── Keyboard Navigation Helpers ────────────────────────────────────────────

    def _smart_solve(self):
        """
        Route the root-level <Return> shortcut to the correct solver.
        Only fires when a method has been selected and the focus is NOT
        inside an individual Entry (those return "break" to stop propagation).
        """
        method = self.method_choice.get()
        if not method or method.startswith('──'):
            return
        if method in _INTERP_METHODS:
            self.solve_interpolation()
        elif method in ['Bisection', 'False Position', 'Newton-Raphson', 'Secant']:
            self.solve_roots()
        else:
            self.solve_system()

    def _on_escape(self, event=None):
        """
        <Escape> handler with Toplevel awareness:
          • If one or more step/explanation Toplevels are open → close the last one.
          • If no Toplevel is open → call setup_interface() to reset the form.

        This prevents Escape from wiping the user's inputs while a results
        window is in the foreground.
        """
        open_toplevels = [
            w for w in self.root.winfo_children()
            if isinstance(w, tk.Toplevel) and w.winfo_exists()
        ]
        if open_toplevels:
            # Close the most recently opened Toplevel
            open_toplevels[-1].destroy()
        else:
            self.setup_interface()

    # ── Background ─────────────────────────────────────────────────────────────

    def resize_bg(self, event):
        """Dynamically resize the background image when the window resizes."""
        if event.widget == self.root:
            w, h = event.width, event.height
            if w > 10 and h > 10:
                resized = self.original_bg_image.resize((w, h), Image.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(resized)
                self.bg_label.config(image=self.bg_photo)

    # ── Interface Setup ────────────────────────────────────────────────────────

    def setup_interface(self, event=None):
        """Clear and rebuild the input area for the selected method."""
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        self.result_label.config(
            text='Ready', fg='yellow',
            font=('Courier New', 48, 'bold')   # restore default font size
        )
        method = self.method_choice.get()
        if not method or method.startswith('──'):
            return
        if method in _INTERP_METHODS:
            self.setup_interpolation_interface()
        elif method in ['Bisection', 'False Position', 'Newton-Raphson', 'Secant']:
            self.setup_roots_interface()
        else:
            self.setup_matrix_interface()

    def setup_roots_interface(self):
        """
        Build the input panel for root-finding methods.

        Keyboard wiring:
          • Enter on each field (except the last) advances focus to the next.
          • Enter on the last field (Epsilon) calls solve_roots().
          • All intermediate bindings return "break" so the root-level
            <Return> → _smart_solve shortcut is NOT triggered prematurely.
        """
        method = self.method_choice.get()
        container = tk.Frame(self.input_frame, bg='#1c1c2e')
        container.pack(pady=40)

        # f(x) entry
        func_frame = tk.Frame(container, bg='#1c1c2e')
        func_frame.pack(pady=10)
        tk.Label(
            func_frame, text='f(x):-',
            font=('Courier New', 16, 'bold'), fg='#00ffcc', bg='#1c1c2e'
        ).pack(side='left', padx=10)
        self.func_entry = tk.Entry(
            func_frame, width=45, font=('Consolas', 16), bd=2, relief='ridge',
            bg='#0f111a', fg='#00ffcc', insertbackground='#00ffcc'
        )
        self.func_entry.pack(side='left')

        inputs_frame = tk.Frame(container, bg='#1c1c2e')
        inputs_frame.pack(pady=20)

        lbl_font   = ('Courier New', 11, 'bold')
        entry_opts = {
            'width': 12, 'font': ('Consolas', 14),
            'bg': '#0f111a', 'fg': '#00ffcc',
            'insertbackground': '#00ffcc', 'bd': 2
        }

        # Collect entries in Tab/Enter traversal order
        ordered_entries = [self.func_entry]

        if method == 'Newton-Raphson':
            tk.Label(inputs_frame, text='Initial Guess (x0):', font=lbl_font,
                     fg='#00ffcc', bg='#1c1c2e').grid(row=0, column=0, padx=10)
            self.x0_entry = tk.Entry(inputs_frame, **entry_opts)
            self.x0_entry.grid(row=0, column=1, padx=10)
            ordered_entries.append(self.x0_entry)

        elif method == 'Secant':
            tk.Label(inputs_frame, text='First Guess (x0):', font=lbl_font,
                     fg='#00ffcc', bg='#1c1c2e').grid(row=0, column=0, padx=10)
            self.x0_entry = tk.Entry(inputs_frame, **entry_opts)
            self.x0_entry.grid(row=0, column=1, padx=10)
            tk.Label(inputs_frame, text='Second Guess (x1):', font=lbl_font,
                     fg='#00ffcc', bg='#1c1c2e').grid(row=0, column=2, padx=10)
            self.x1_entry = tk.Entry(inputs_frame, **entry_opts)
            self.x1_entry.grid(row=0, column=3, padx=10)
            ordered_entries.extend([self.x0_entry, self.x1_entry])

        else:  # Bisection / False Position
            tk.Label(inputs_frame, text='Start Point (a):', font=lbl_font,
                     fg='#00ffcc', bg='#1c1c2e').grid(row=0, column=0, padx=10)
            self.a_entry = tk.Entry(inputs_frame, **entry_opts)
            self.a_entry.grid(row=0, column=1, padx=10)
            tk.Label(inputs_frame, text='End Point (b):', font=lbl_font,
                     fg='#00ffcc', bg='#1c1c2e').grid(row=0, column=2, padx=10)
            self.b_entry = tk.Entry(inputs_frame, **entry_opts)
            self.b_entry.grid(row=0, column=3, padx=10)
            ordered_entries.extend([self.a_entry, self.b_entry])

        # Epsilon (always present)
        tk.Label(inputs_frame, text='Epsilon:', font=lbl_font,
                 fg='#00ffcc', bg='#1c1c2e').grid(row=1, column=0, padx=10, pady=15)
        self.eps_entry = tk.Entry(inputs_frame, **entry_opts)
        self.eps_entry.insert(0, '0.0001')
        self.eps_entry.grid(row=1, column=1, padx=10, pady=15)
        ordered_entries.append(self.eps_entry)

        # ── Wire Enter-advances-focus chain ───────────────────────────────
        # Each intermediate entry's <Return> moves focus to the next field
        # and returns "break" so the root-level shortcut does NOT also fire.
        for idx, entry in enumerate(ordered_entries[:-1]):
            nxt = ordered_entries[idx + 1]
            def _advance(e, nxt=nxt):
                nxt.focus_set()
                return "break"
            entry.bind('<Return>', _advance)

        # Last entry (Epsilon): Enter → solve directly
        ordered_entries[-1].bind('<Return>', lambda e: self.solve_roots())

        # ── Buttons ───────────────────────────────────────────────────────
        buttons_frame = tk.Frame(container, bg='#1c1c2e')
        buttons_frame.pack(pady=30)
        tk.Button(
            buttons_frame, text='Solve System', command=self.solve_roots,
            bg='#27ae60', fg='white', font=('Courier New', 14, 'bold'),
            width=18, height=2, cursor='hand2'
        ).pack(side='left', padx=10)
        tk.Button(
            buttons_frame, text='Clear', command=self.setup_interface,
            bg='#e74c3c', fg='white', font=('Courier New', 14, 'bold'),
            width=18, height=2, cursor='hand2'
        ).pack(side='left', padx=10)

        # Start focus on the function entry for immediate typing
        self.func_entry.focus_set()

    # ── Interpolation Interface (added) ───────────────────────────────────────

    def setup_interpolation_interface(self):
        """
        Build the input panel for all interpolation methods.

        Layout:
          Row 0 : Number of data points  +  [Generate Table] button
          Row 1 : Dynamic x/y table (Entry grid)
          Row 2 : Target x  (or Target y for Lagrange Inverse)
          Row 3 : Step size h  (only for Newton Forward/Backward/Stirling)
          Row 4 : [Solve] [Clear] buttons
        """
        method = self.method_choice.get()
        container = tk.Frame(self.input_frame, bg='#1c1c2e')
        container.pack(fill='both', expand=True, pady=20, padx=20)

        # ── Title ──────────────────────────────────────────────────────────
        tk.Label(
            container, text=f'Interpolation  ⟶  {method}',
            font=('Courier New', 14, 'bold'), fg='#00ffcc', bg='#1c1c2e'
        ).pack(pady=(0, 10))

        # ── Row 0: n selector ──────────────────────────────────────────────
        n_frame = tk.Frame(container, bg='#1c1c2e')
        n_frame.pack(pady=6)
        tk.Label(
            n_frame, text='Number of data points (n):',
            font=('Courier New', 11, 'bold'), fg='#00ffcc', bg='#1c1c2e'
        ).pack(side='left', padx=6)
        self.interp_n_entry = tk.Entry(
            n_frame, width=6, font=('Consolas', 13),
            bg='#0f111a', fg='#00ffcc', insertbackground='#00ffcc', bd=2
        )
        self.interp_n_entry.pack(side='left', padx=6)
        tk.Button(
            n_frame, text='Generate Table',
            command=self._generate_interp_table,
            bg='#2980b9', fg='white',
            font=('Courier New', 10, 'bold'), padx=10, cursor='hand2'
        ).pack(side='left', padx=6)
        self.interp_n_entry.bind('<Return>', lambda e: self._generate_interp_table())
        self.interp_n_entry.focus_set()

        # ── Row 1: table container (populated by _generate_interp_table) ───
        self.interp_table_frame = tk.Frame(container, bg='#1c1c2e')
        self.interp_table_frame.pack(pady=10)

        # ── Row 2: Target value ────────────────────────────────────────────
        target_frame = tk.Frame(container, bg='#1c1c2e')
        target_frame.pack(pady=6)
        target_lbl = 'Target y (find x):' if method == 'Lagrange Inverse' else 'Target x (find y):'
        tk.Label(
            target_frame, text=target_lbl,
            font=('Courier New', 11, 'bold'), fg='#00ffcc', bg='#1c1c2e'
        ).pack(side='left', padx=6)
        self.interp_target_entry = tk.Entry(
            target_frame, width=14, font=('Consolas', 13),
            bg='#0f111a', fg='#00ffcc', insertbackground='#00ffcc', bd=2
        )
        self.interp_target_entry.pack(side='left', padx=6)

        # ── Row 3: Step size h (Newton / Stirling only) ────────────────────
        needs_h = method in ('Newton Forward', 'Newton Backward', 'Stirling')
        self.interp_h_entry = None
        if needs_h:
            h_frame = tk.Frame(container, bg='#1c1c2e')
            h_frame.pack(pady=6)
            tk.Label(
                h_frame, text='Step size h (leave blank to auto-compute):',
                font=('Courier New', 11, 'bold'), fg='#b8b8d0', bg='#1c1c2e'
            ).pack(side='left', padx=6)
            self.interp_h_entry = tk.Entry(
                h_frame, width=10, font=('Consolas', 13),
                bg='#0f111a', fg='#00ffcc', insertbackground='#00ffcc', bd=2
            )
            self.interp_h_entry.pack(side='left', padx=6)

        # ── Row 4: Solve / Clear ───────────────────────────────────────────
        btn_frame = tk.Frame(container, bg='#1c1c2e')
        btn_frame.pack(pady=20)
        tk.Button(
            btn_frame, text='Solve', command=self.solve_interpolation,
            bg='#27ae60', fg='white',
            font=('Courier New', 14, 'bold'), width=16, height=2, cursor='hand2'
        ).pack(side='left', padx=10)
        tk.Button(
            btn_frame, text='Clear', command=self.setup_interface,
            bg='#e74c3c', fg='white',
            font=('Courier New', 14, 'bold'), width=16, height=2, cursor='hand2'
        ).pack(side='left', padx=10)

        # Store method for later use by _generate_interp_table / solve_interpolation
        self._interp_method = method
        self._interp_x_entries = []
        self._interp_y_entries = []

    def _generate_interp_table(self):
        """Build the x / y entry grid inside interp_table_frame."""
        for w in self.interp_table_frame.winfo_children():
            w.destroy()
        self._interp_x_entries = []
        self._interp_y_entries = []

        try:
            n = int(self.interp_n_entry.get())
            if n < 2:
                raise ValueError('Need at least 2 data points.')
            if n > 20:
                raise ValueError('Maximum 20 data points for display.')
        except ValueError as exc:
            messagebox.showerror('Input Error', str(exc))
            return

        entry_opts = dict(
            width=12, font=('Consolas', 12), justify='center',
            bg='#0f111a', fg='#00ffcc', insertbackground='#00ffcc', bd=2
        )

        # Header row
        tk.Label(
            self.interp_table_frame, text='i',
            font=('Courier New', 10, 'bold'), fg='#7f8c8d', bg='#1c1c2e', width=4
        ).grid(row=0, column=0, padx=4, pady=3)
        tk.Label(
            self.interp_table_frame, text='x',
            font=('Courier New', 10, 'bold'), fg='#00ffcc', bg='#1c1c2e', width=12
        ).grid(row=0, column=1, padx=4, pady=3)
        tk.Label(
            self.interp_table_frame, text='y  =  f(x)',
            font=('Courier New', 10, 'bold'), fg='#f39c12', bg='#1c1c2e', width=14
        ).grid(row=0, column=2, padx=4, pady=3)

        for i in range(n):
            tk.Label(
                self.interp_table_frame, text=str(i),
                font=('Courier New', 10), fg='#7f8c8d', bg='#1c1c2e'
            ).grid(row=i + 1, column=0, padx=4)
            ex = tk.Entry(self.interp_table_frame, **entry_opts)
            ex.grid(row=i + 1, column=1, padx=6, pady=3)
            ey = tk.Entry(self.interp_table_frame, **entry_opts)
            ey.config(fg='#f39c12')
            ey.grid(row=i + 1, column=2, padx=6, pady=3)
            self._interp_x_entries.append(ex)
            self._interp_y_entries.append(ey)

        # Wire Enter navigation through the table cells
        all_cells = []
        for i in range(n):
            all_cells.append(self._interp_x_entries[i])
            all_cells.append(self._interp_y_entries[i])
        for idx, cell in enumerate(all_cells[:-1]):
            nxt = all_cells[idx + 1]
            cell.bind('<Return>', lambda e, nxt=nxt: (nxt.focus_set(), 'break')[1])
        all_cells[-1].bind('<Return>', lambda e: self.solve_interpolation())
        if all_cells:
            all_cells[0].focus_set()

    def solve_interpolation(self):
        """Gather table data, call the chosen interpolation module, display result."""
        method = getattr(self, '_interp_method', self.method_choice.get())

        if not HAS_INTERP:
            messagebox.showerror('Error', 'Interpolation modules could not be loaded.')
            return

        if not self._interp_x_entries:
            messagebox.showerror('Error', 'Please generate the data table first.')
            return

        try:
            x_vals = [float(e.get()) for e in self._interp_x_entries]
            y_vals = [float(e.get()) for e in self._interp_y_entries]
        except ValueError:
            messagebox.showerror('Input Error', 'All x and y cells must contain valid numbers.')
            return

        try:
            target_raw = self.interp_target_entry.get().strip()
            if not target_raw:
                messagebox.showerror('Input Error', 'Please enter a target value.')
                return
            target = float(target_raw)
        except ValueError:
            messagebox.showerror('Input Error', 'Target value must be a number.')
            return

        # Optional h
        h = None
        if self.interp_h_entry is not None:
            h_raw = self.interp_h_entry.get().strip()
            if h_raw:
                try:
                    h = float(h_raw)
                except ValueError:
                    messagebox.showerror('Input Error', 'Step size h must be a number.')
                    return

        try:
            if method == 'Newton Forward':
                res_dict = newton_forward.solve(x_vals, y_vals, target, h)
            elif method == 'Newton Backward':
                res_dict = newton_backward.solve(x_vals, y_vals, target, h)
            elif method == 'Stirling':
                res_dict = stirling.solve(x_vals, y_vals, target, h)
            elif method == 'Lagrange':
                res_dict = lagrange.solve(x_vals, y_vals, target)
            elif method == 'Lagrange Inverse':
                res_dict = lagrange_inverse.solve(x_vals, y_vals, target)
            else:
                raise ValueError(f'Unknown interpolation method: {method}')
        except Exception as exc:
            messagebox.showerror('Computation Error', str(exc))
            return

        result     = res_dict['result']
        steps      = res_dict['steps']
        explanation = res_dict['explanation']

        # ── Result banner ──────────────────────────────────────────────────
        self.result_label.config(
            text=self.fmt(result), fg='#00ffcc',
            font=('Courier New', 42, 'bold')
        )

        # ── Steps window ───────────────────────────────────────────────────
        self._show_interp_steps(method, steps, explanation)

        self.log_operation(
            method,
            f"x={x_vals}, y={y_vals}, target={target}",
            f"result={self.fmt(result)}"
        )

    def _show_interp_steps(self, method, steps, explanation):
        """Open a styled Toplevel showing the interpolation step log."""
        win = tk.Toplevel(self.root)
        win.title(f'Interpolation Steps — {method}')
        win.geometry('820x560')
        win.configure(bg='#2c3e50')
        win.bind('<Escape>', lambda e: win.destroy())

        # ── Steps text area ────────────────────────────────────────────────
        tk.Label(
            win, text='Step-by-Step Computation',
            font=('Courier New', 13, 'bold'), fg='#00ffcc', bg='#2c3e50'
        ).pack(anchor='w', padx=15, pady=(12, 4))

        steps_txt = tk.Text(
            win, font=('Consolas', 10), wrap='word',
            bg='#0f111a', fg='white', padx=12, pady=10,
            insertbackground='#00ffcc', height=15
        )
        steps_txt.pack(fill='both', expand=True, padx=15, pady=(0, 6))
        for line in steps:
            steps_txt.insert(tk.END, line + '\n')
        steps_txt.config(state='disabled')

        # ── Explanation area ───────────────────────────────────────────────
        tk.Label(
            win, text='Explanation',
            font=('Courier New', 12, 'bold'), fg='#f39c12', bg='#2c3e50'
        ).pack(anchor='w', padx=15, pady=(6, 2))

        expl_txt = tk.Text(
            win, font=('Segoe UI', 10), wrap='word',
            bg='#1a2636', fg='#ecf0f1', padx=12, pady=8,
            insertbackground='#00ffcc', height=5
        )
        expl_txt.pack(fill='x', padx=15, pady=(0, 12))
        expl_txt.insert(tk.END, explanation)
        expl_txt.config(state='disabled')

        tk.Button(
            win, text='Close  [Esc]', command=win.destroy,
            bg='#e74c3c', fg='white',
            font=('Courier New', 11, 'bold'), padx=20, pady=4, cursor='hand2'
        ).pack(pady=(0, 14))

    def setup_matrix_interface(self):
        """Build the dimension-selector panel for matrix-based methods."""
        dim_frame = tk.Frame(self.input_frame, bg='white')
        dim_frame.pack(pady=30)
        tk.Label(
            dim_frame, text='Enter Matrix Size (n):',
            font=('Segoe UI', 12, 'bold'), bg='white'
        ).pack(side='left', padx=10)
        self.dim_entry = tk.Entry(dim_frame, width=10, font=('Consolas', 13), bd=2)
        self.dim_entry.pack(side='left', padx=10)

        # Enter on the dim entry generates the grid (no need to click)
        self.dim_entry.bind('<Return>', lambda e: self.generate_matrix_grid())
        self.dim_entry.focus_set()

        tk.Button(
            dim_frame, text='GENERATE GRID', command=self.generate_matrix_grid,
            bg='#2980b9', fg='white', font=('Segoe UI', 10, 'bold'), padx=15
        ).pack(side='left', padx=10)
        tk.Button(
            dim_frame, text='RESET', command=self.setup_interface,
            bg='#e74c3c', fg='white', font=('Segoe UI', 10, 'bold'), padx=15
        ).pack(side='left', padx=10)

        self.grid_container = tk.Frame(self.input_frame, bg='white')
        self.grid_container.pack(pady=20)

    # ── Logging ────────────────────────────────────────────────────────────────

    def log_operation(self, method, inputs, result):
        """Append a timestamped entry to the operations history file."""
        try:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = (
                f"[{timestamp}] Method: {method}\n"
                f"Inputs: {inputs}\n"
                f"Result: {result}\n"
                f"{'-' * 40}\n"
            )
            with open("operations_history.txt", "a") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Failed to log operation: {e}")

    # ── Matrix Grid ────────────────────────────────────────────────────────────

    def generate_matrix_grid(self):
        """
        Build the n×n matrix entry grid with:
          • A 'Fill Empty Cells with Zeros' button
          • Epsilon row (iterative methods only)
          • Full Tab/Enter keyboard navigation chain
        """
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        # Remove stale suggest_label reference so it is rebuilt fresh
        if hasattr(self, 'suggest_label'):
            del self.suggest_label

        try:
            val = self.dim_entry.get()
            if not val:
                return
            n = int(val)
            if n > 10:
                raise ValueError('Size too large for display (max 10)')

            self.matrix_entries = []
            self.vector_entries = []

            # ── Column headers ────────────────────────────────────────────
            for j in range(n):
                tk.Label(
                    self.grid_container, text=f'X{to_subscript(j + 1)}',
                    font=('Segoe UI', 10, 'bold'), fg='#00ffcc', bg='#1c1c2e'
                ).grid(row=0, column=j)
            tk.Label(
                self.grid_container, text=' | Result (B)',
                font=('Segoe UI', 10, 'bold'), fg='red', bg='#1c1c2e'
            ).grid(row=0, column=n)

            # ── Matrix entry cells & B-vector ─────────────────────────────
            for i in range(n):
                row_entries = []
                for j in range(n):
                    e = tk.Entry(
                        self.grid_container, width=10,
                        font=('Consolas', 12), justify='center',
                        bd=2, bg='#0f111a', fg='#00ffcc'
                    )
                    e.grid(row=i + 1, column=j, padx=4, pady=4)
                    e.bind('<KeyRelease>', self.check_matrix_properties)
                    row_entries.append(e)
                self.matrix_entries.append(row_entries)

                be = tk.Entry(
                    self.grid_container, width=10,
                    font=('Consolas', 12, 'bold'), fg='red',
                    justify='center', bd=2, bg='#0f111a'
                )
                be.grid(row=i + 1, column=n, padx=15, pady=4)
                self.vector_entries.append(be)

            # ── Epsilon (iterative methods only) ──────────────────────────
            if self.method_choice.get() in ['Jacobi', 'Gauss-Seidel']:
                eps_frame = tk.Frame(self.grid_container, bg='#1c1c2e')
                eps_frame.grid(row=n + 2, column=0, columnspan=n + 1, pady=15)
                tk.Label(
                    eps_frame, text='Error Rate (Epsilon):',
                    font=('Segoe UI', 11, 'bold'), fg='#00ffcc', bg='#1c1c2e'
                ).pack(side='left', padx=5)
                self.eps_matrix_entry = tk.Entry(
                    eps_frame, width=15, font=('Consolas', 12),
                    bd=2, bg='#0f111a', fg='#00ffcc'
                )
                self.eps_matrix_entry.insert(0, '0.0001')
                self.eps_matrix_entry.pack(side='left')

            # ── Fill Empty Cells with Zeros button ────────────────────────
            # Sits between Epsilon and Solve for a natural Tab flow.
            # Clicking (or pressing Enter when focused) fills only blank cells.
            fill_btn = tk.Button(
                self.grid_container,
                text='⓪  Fill Empty Cells with Zeros',
                command=self._fill_zeros,
                bg='#2c3e50', fg='#00ffcc',
                font=('Courier New', 10, 'bold'),
                width=30, height=1,
                cursor='hand2', relief='flat',
                activebackground='#34495e', activeforeground='#00ffcc'
            )
            fill_btn.grid(row=n + 3, column=0, columnspan=n + 1, pady=(5, 0))

            # ── Solve button ──────────────────────────────────────────────
            solve_btn = tk.Button(
                self.grid_container,
                text='Solve System',
                command=self.solve_system,
                bg='#27ae60', fg='white',
                font=('Courier New', 12, 'bold'),
                width=30, height=2,
                cursor='hand2'
            )
            solve_btn.grid(row=n + 4, column=0, columnspan=n + 1, pady=20)

            # ── Wire Tab/Enter navigation through the entire grid ─────────
            self._wire_matrix_tab_chain(n, fill_btn, solve_btn)

        except ValueError as e:
            messagebox.showerror('Error', str(e))

    def _wire_matrix_tab_chain(self, n, fill_btn, solve_btn):
        """
        Configure keyboard navigation for the matrix entry grid.

        Strategy:
          • Tkinter handles Tab naturally for all intermediate cells.
          • We only override: last B-vector cell → Tab → fill_btn → Tab → solve_btn.
          • Enter on each cell advances to the next cell (returning "break" so
            the root-level <Return> → _smart_solve does not also fire).
          • Enter on the last cell calls solve_system().
          • Enter on fill_btn triggers _fill_zeros(); Enter on solve_btn solves.
        """
        # Flatten entries in visual order: A[row][col] followed by B[row]
        all_entries = []
        for i in range(n):
            all_entries.extend(self.matrix_entries[i])
            all_entries.append(self.vector_entries[i])

        # Enter on each entry (except the last) advances focus
        for idx, entry in enumerate(all_entries[:-1]):
            nxt = all_entries[idx + 1]
            def _advance(e, nxt=nxt):
                nxt.focus_set()
                return "break"   # stop root-level <Return> from also firing
            entry.bind('<Return>', _advance)

        # Last entry: Enter → solve
        all_entries[-1].bind('<Return>', lambda e: self.solve_system())

        # Tab override: last matrix cell → Fill button
        def _tab_to_fill(e):
            fill_btn.focus_set()
            return "break"
        all_entries[-1].bind('<Tab>', _tab_to_fill)

        # Tab override: Fill button → Solve button
        def _tab_to_solve(e):
            solve_btn.focus_set()
            return "break"
        fill_btn.bind('<Tab>', _tab_to_solve)

        # Enter on Fill button → trigger fill action
        fill_btn.bind('<Return>', lambda e: self._fill_zeros())

        # Enter on Solve button → solve
        solve_btn.bind('<Return>', lambda e: self.solve_system())

        # Place initial focus on the first matrix cell
        if self.matrix_entries:
            self.matrix_entries[0][0].focus_set()

    # ── Auto-Fill Zeros ────────────────────────────────────────────────────────

    def _fill_zeros(self):
        """
        Fill every empty cell in the matrix grid and the B-vector with '0'.

        Rules:
          • Only blank (whitespace-only) cells are filled — existing values
            are always preserved.
          • Newly filled cells flash with a brief green tint for visual feedback,
            then restore to the standard dark background.
        """
        def _flash(entry, restore_bg='#0f111a'):
            """Green tint for 600 ms, then restore the original background."""
            entry.config(bg='#1a3a1a')
            entry.after(600, lambda: entry.config(bg=restore_bg))

        for row in self.matrix_entries:
            for entry in row:
                if not entry.get().strip():
                    entry.insert(0, '0')
                    _flash(entry)

        for entry in self.vector_entries:
            if not entry.get().strip():
                entry.insert(0, '0')
                _flash(entry)   # B-vector uses red fg; bg restore is the same

    # ── Solvers ────────────────────────────────────────────────────────────────

    def solve_roots(self):
        """
        Gather inputs, call the selected root-finding method, and display
        the result using the current precision setting (self.fmt).
        """
        method = self.method_choice.get()
        try:
            f   = self.func_entry.get()
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

            # ── Display result with current precision ─────────────────────
            self.result_label.config(
                text=self.fmt(res), fg='yellow',
                font=('Courier New', 48, 'bold')
            )
            self.display_steps(df, method)
            display_f = f.replace('sqrt', '√')
            self.plot_function(f, res, df)
            self.log_operation(
                method,
                f"f(x)={display_f}, eps={eps}",
                f"Root={self.fmt(res)}, iters={iters}"
            )
        except Exception as e:
            messagebox.showerror('Math Error', str(e))

    def solve_system(self):
        """
        Gather matrix inputs, call the selected linear-system method, and
        display the solution vector in the result banner using self.fmt.
        """
        method = self.method_choice.get()
        try:
            n   = len(self.matrix_entries)
            A   = [[float(self.matrix_entries[i][j].get()) for j in range(n)] for i in range(n)]
            B   = [float(self.vector_entries[i].get()) for i in range(n)]
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
                df = pd.DataFrame(
                    res.reshape(1, -1),
                    columns=[f'X{to_subscript(i+1)}' for i in range(len(res))]
                )

            # ── Build formatted solution vector for the result banner ─────
            # Shrink the font for longer vectors so entries fit on one line.
            font_size = 24 if n > 4 else 32
            formatted_vec = "  ".join(
                [f"X{to_subscript(i+1)}={self.fmt(v)}" for i, v in enumerate(res)]
            )
            self.result_label.config(
                text=formatted_vec, fg='yellow',
                font=('Courier New', font_size, 'bold')
            )
            self.display_steps(df, method)
            self.plot_matrix_convergence(df, method, res)
            self.log_operation(method, f"Matrix size {n}x{n}", formatted_vec)

        except Exception as e:
            messagebox.showerror('Input Error', f'Check inputs: {str(e)}')

    # ── Step Display ───────────────────────────────────────────────────────────

    def display_steps(self, df, method):
        """
        Open a Toplevel Treeview with the iteration history.
        All float values are formatted with self.fmt() so the table respects
        the user's current precision setting.
        Escape closes this window.
        """
        if df is None:
            return

        table_win = tk.Toplevel(self.root)
        table_win.title('Step-by-Step Numerical Analysis')
        table_win.geometry('800x500')
        table_win.configure(bg='#2c3e50')

        # Escape closes this specific window (not the whole app)
        table_win.bind('<Escape>', lambda e: table_win.destroy())

        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            'Treeview',
            font=('Segoe UI', 10), rowheight=25,
            background='#2c3e50', fieldbackground='#2c3e50', foreground='white'
        )
        style.configure(
            'Treeview.Heading',
            font=('Segoe UI', 10, 'bold'),
            background='#0f111a', foreground='#00ffcc'
        )
        style.map('Treeview', background=[('selected', '#34495e')])

        tree = ttk.Treeview(table_win, style='Treeview')
        tree['columns'] = list(df.columns)
        tree['show']    = 'headings'
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor='center')

        for (_, row) in df.iterrows():
            formatted_row = []
            for col, val in row.items():
                if col == 'Iteration':
                    # Iteration is always an integer — no precision formatting
                    formatted_row.append(int(val))
                elif isinstance(val, (float, np.floating)):
                    # Apply the user's precision setting to every numeric cell
                    formatted_row.append(self.fmt(val))
                else:
                    formatted_row.append(val)
            tree.insert('', 'end', values=formatted_row)

        vsb = ttk.Scrollbar(table_win, orient='vertical',   command=tree.yview)
        hsb = ttk.Scrollbar(table_win, orient='horizontal', command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.pack(expand=True, fill='both')
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')

        btn_frame = tk.Frame(table_win, bg='#2c3e50')
        btn_frame.pack(pady=10)
        tk.Button(
            btn_frame, text="View Steps Explanation",
            command=lambda: self.explain_steps(df, method),
            bg='#e74c3c', fg='white',
            font=('Courier New', 12, 'bold'),
            relief='flat', padx=15, pady=5, cursor='hand2'
        ).pack()

    # ── Matrix Property Checker ────────────────────────────────────────────────

    def check_matrix_properties(self, event=None):
        """
        Detect tridiagonal or diagonally-dominant structure after each keystroke
        and display a method suggestion label below the grid.
        The suggest_label is placed at row n+5 (below the Solve button).
        """
        if not hasattr(self, 'suggest_label'):
            n = len(self.matrix_entries)
            self.suggest_label = tk.Label(
                self.grid_container, text='',
                font=('Segoe UI', 11, 'bold'), fg='#d35400', bg='white'
            )
            # Row n+5: header(0) + n data rows + eps(n+2) + fill(n+3) + solve(n+4)
            self.suggest_label.grid(row=n + 5, column=0, columnspan=n + 1, pady=5)

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

            if is_tridiag and n > 1:
                super_diag_nonzero = any(abs(A[i, i + 1]) > 0 for i in range(n - 1))
                sub_diag_nonzero   = any(abs(A[i + 1, i]) > 0 for i in range(n - 1))
                if super_diag_nonzero or sub_diag_nonzero:
                    self.suggest_label.config(
                        text="✨ Suggested Method: Thomas Algorithm (Tridiagonal Detected) ✨"
                    )
                    return

            # Check Diagonal Dominance
            is_diag_dom = True
            for i in range(n):
                diag       = abs(A[i, i])
                sum_others = sum(abs(A[i, j]) for j in range(n) if i != j)
                if diag <= sum_others:
                    is_diag_dom = False
                    break

            if is_diag_dom:
                self.suggest_label.config(
                    text="✨ Suggested Method: Gauss-Seidel or Jacobi (Diagonally Dominant) ✨"
                )
                return

            self.suggest_label.config(text="")
        except ValueError:
            self.suggest_label.config(text="")

    # ── Step Explanations ──────────────────────────────────────────────────────

    def explain_steps(self, df, method):
        """
        Open a Toplevel with a human-readable walkthrough of each iteration.
        All numeric values are formatted with self.fmt() for consistency.
        Escape closes this window.
        """
        explain_win = tk.Toplevel(self.root)
        explain_win.title(f"Step Explanations - {method}")
        explain_win.geometry('700x500')
        explain_win.configure(bg='#2c3e50')
        explain_win.bind('<Escape>', lambda e: explain_win.destroy())

        text_widget = tk.Text(
            explain_win, font=('Segoe UI', 11), wrap='word',
            bg='#0f111a', fg='white', padx=15, pady=15,
            insertbackground='#00ffcc'
        )
        text_widget.pack(expand=True, fill='both', padx=10, pady=10)

        explanations = []

        if method == "Bisection":
            for _, row in df.iterrows():
                explanations.append(
                    f"Iteration {int(row['Iteration'])}: "
                    f"Evaluated midpoint c = {self.fmt(row['c (Midpoint)'])}. "
                    f"The function value f(c) = {self.fmt(row['f(c)'])}. "
                    f"The bounds were updated from "
                    f"[a={self.fmt(row['a'])}, b={self.fmt(row['b'])}] "
                    f"to narrow the search bracket."
                )

        elif method == "Newton-Raphson":
            for _, row in df.iterrows():
                deriv  = row.get("f'(xₙ)", 0)
                next_x = row.get("xₙ₊₁", row['xₙ'])
                explanations.append(
                    f"Iteration {int(row['Iteration'])}: "
                    f"Starting at xₙ = {self.fmt(row['xₙ'])}, "
                    f"evaluated f(xₙ) = {self.fmt(row['f(xₙ)'])} "
                    f"and derivative f'(xₙ) = {self.fmt(deriv)}. "
                    f"Calculated next approximation xₙ₊₁ = {self.fmt(next_x)}."
                )

        elif method == "Secant":
            # Note: the Secant history stores 'xₙ' (current) and 'xₙ₊₁' (next).
            # There is no 'xₙ₋₁' column; we use 'xₙ' as the current anchor.
            for _, row in df.iterrows():
                explanations.append(
                    f"Iteration {int(row['Iteration'])}: "
                    f"Current approximation xₙ = {self.fmt(row['xₙ'])}. "
                    f"f(xₙ) = {self.fmt(row['f(xₙ)'])}. "
                    f"Next approximation xₙ₊₁ = {self.fmt(row['xₙ₊₁'])}."
                )

        elif method == "False Position":
            for _, row in df.iterrows():
                explanations.append(
                    f"Iteration {int(row['Iteration'])}: "
                    f"Calculated intersection point xs = {self.fmt(row['xs'])}. "
                    f"Evaluated f(xs) = {self.fmt(row['f(xs)'])}. "
                    f"Updated brackets [a={self.fmt(row['a'])}, b={self.fmt(row['b'])}]."
                )

        elif method in ["Jacobi", "Gauss-Seidel"]:
            for idx, row in df.iterrows():
                var_str = ", ".join(
                    f"{col} = {self.fmt(row[col])}"
                    for col in df.columns if col != 'Iteration'
                )
                explanations.append(
                    f"Iteration {idx}: Updated variables closer to exact solution. {var_str}"
                )

        elif method == "Thomas Algorithm":
            explanations.append(
                "Thomas Algorithm is an exact method (no iterations). It executes in three steps:"
            )
            explanations.append("1. Forward Sweep to eliminate the lower diagonal (Intermediate y).")
            explanations.append("2. Process the B array (Intermediate z).")
            explanations.append("3. Back Substitution to find the Final Solution x.")

        elif method == "Doolittle":
            explanations.append(
                "Doolittle factorization splits the matrix into Lower (L) and Upper (U) triangular matrices."
            )
            explanations.append("Then solves Ly = B, and finally Ux = y to obtain the result.")

        for p in explanations:
            text_widget.insert(tk.END, p + "\n\n")
        text_widget.config(state='disabled')

    # ── Plot Helpers ───────────────────────────────────────────────────────────

    def plot_function(self, func_str, root_val, df):
        """Render the function curve and highlight the found root (right panel)."""
        if not HAS_MATPLOTLIB:
            return

        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        try:
            x = sp.symbols('x')
            local_dict = {
                'pi': sp.pi, 'e': sp.E, 'exp': sp.exp,
                'cos': sp.cos, 'sin': sp.sin, 'tan': sp.tan, 'sqrt': sp.sqrt
            }
            transformations = standard_transformations + (
                implicit_multiplication_application, convert_xor
            )
            expr   = parse_expr(func_str, local_dict=local_dict, transformations=transformations)
            f_lamb = sp.lambdify(x, expr, "numpy")

            fig = Figure(figsize=(5, 4), dpi=100)
            ax  = fig.add_subplot(111)

            x_vals = []
            if 'a' in df.columns and 'b' in df.columns:
                x_vals.extend(df['a'].tolist())
                x_vals.extend(df['b'].tolist())
            elif 'xₙ' in df.columns:
                x_vals.extend(df['xₙ'].tolist())
            elif 'xn' in df.columns:
                x_vals.extend(df['xn'].tolist())

            if x_vals:
                min_x, max_x = min(x_vals) - 1, max(x_vals) + 1
            else:
                min_x, max_x = root_val - 5, root_val + 5

            X_plot = np.linspace(min_x, max_x, 400)
            Y_plot = f_lamb(X_plot)

            display_f = func_str.replace('sqrt', '√')
            ax.plot(X_plot, Y_plot, label=f'f(x)={display_f}', color='#2980b9')
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(X_plot[0], color='black', linewidth=1)
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
        """
        Right-panel plot:
          • Iterative methods → convergence lines per variable.
          • Exact methods     → bar chart of the solution vector.
        """
        if not HAS_MATPLOTLIB:
            return

        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(5, 4), dpi=100)
        ax  = fig.add_subplot(111)

        if method in ['Jacobi', 'Gauss-Seidel']:
            for col in df.columns:
                ax.plot(df.index, df[col], marker='o', label=col)
            ax.set_title(f"Convergence of {method}")
            ax.set_xlabel("Iteration")
            ax.set_ylabel("Value")
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.6)
        else:
            res_vector = final_res[0] if isinstance(final_res, tuple) else final_res
            x_pos = np.arange(len(res_vector))
            ax.bar(x_pos, res_vector, align='center', alpha=0.7, color='#27ae60')
            ax.set_xticks(x_pos)
            ax.set_xticklabels([f"X{to_subscript(i+1)}" for i in range(len(res_vector))])
            ax.set_title("Final Solution Vector")
            ax.set_ylabel("Value")
            ax.grid(True, axis='y', linestyle='--', alpha=0.6)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
