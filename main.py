from fractions import Fraction
import sympy as sp
def TypeOferrors( XE ,  XA):
    try:
        
        EA = abs(XE - XA)
        print(f"The Absolute erro 'EA' = {EA}")
        ER = abs(EA / XE)
        print(f"The Relative error 'ER' = {ER}")
        EP = 100 * ER
        print(f"The percentage relative error 'EP' = {EP}")


        """
        In This step I Cant calculate the SD 

        """
        # ask = int(input("if you want Significant digits? \n for yes enter 1 for no enter 0 \n "))
        # if ask == 1 :
        #     x = 0 
        #     sd = 0
        #     while True:

        #        if ER > 5 * (10**(-x)):
        #         sd = x
                
                
        #        elif(ER < 5 * (10**(-x))):
                   
        #            print(f"The Significant Digits = {sd} \n")
        #            break
                   
        #        else:
        #           x+=1



    except ValueError():
        print("Pleas Ente Float Number Correct  \n")

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
