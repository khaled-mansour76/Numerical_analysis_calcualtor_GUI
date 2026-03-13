from fractions import Fraction
import sympy as sp
def calculate_condition_number(equation, A):
    x = sp.symbols('x')  #define X
    
    try:
        f = sp.sympify(equation)  #transform the string to equation
    except:
        return ("EX. sin x -> sin(x)")
    
    d = sp.diff(f, x)
    
    try:
        Ae = float(sp.sympify(A, locals={'pi': sp.pi}).evalf())
    except:
        return ("Enter A correct Ex. 𝜋 -> pi")

    r1 = f.subs(x, Ae).evalf()  #calculate f(a)
    r2 = d.subs(x, Ae).evalf()  #calclate f'(a)
    
    if r1 == 0:
        return("f(a) = 0")
    

    print(f"The Original  Function -> {f} \n ") ; print(f"The Derintive Function -> {d} \n") ; print(f"a Value {Ae} Original a {A}")
    

    result = abs((Ae * r2) / r1)
    return float(result)