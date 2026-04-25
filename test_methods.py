import secant
import newton_rapson

f = "x^2 - 4"
root, iters, df = secant.Secant(f, 1, 3, 1e-4)
print("Secant DF:")
if df is not None:
    print(df)

root, iters, df = newton_rapson.Newton_Raphson(f, 1, 1e-4)
print("\nNewton Raphson DF:")
if df is not None:
    print(df)
