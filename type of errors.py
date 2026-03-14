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
        print("Pleas Enter Float Number Correct  \n")



print("I am finished")

