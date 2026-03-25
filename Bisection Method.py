import sympy as sp

def Bisection(func, a_val, b_val):
    x = sp.symbols('x')
    local_dict = {'pi': sp.pi, 'e': sp.E, 'exp': sp.exp}
    try:
        f = sp.sympify(func , locals=local_dict )
    except:
        return "Check your function syntax (e.g., use sin(x) instead of sin x)"

    fa = f.subs(x, a_val).evalf()
    fb = f.subs(x, b_val).evalf()

    if fa * fb >= 0:
        return "Bisection method fails. f(a) and f(b) must have opposite signs."

    a = [a_val]
    b = [b_val]
    c = []
    iteration = 0
    tolerance = 0.0001

    while True:
        iteration += 1
        current_c = (a[-1] + b[-1]) / 2
        c.append(current_c)
        
        fc = f.subs(x, current_c).evalf()

        if abs(fc) < 1e-10 or (len(c) > 1 and abs(c[-1] - c[-2]) < tolerance):
            break

        if (f.subs(x, a[-1]).evalf() * fc) < 0:
            a.append(a[-1])
            b.append(current_c)
        else:
            a.append(current_c)
            b.append(b[-1])

    print(f"Root found: {c[-1]}")
    print(f"Total iterations: {iteration} '\n' " )

func = "x**6 - x - 1" 
Bisection(func, 1, 2)