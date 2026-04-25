import secant
import gui_module

f = "x^2 - 4"
root, iters, df = secant.Secant(f, 1, 3, 1e-4)
print("Testing explain_steps for Secant")
exps = []
for _, row in df.iterrows():
    exps.append(f"Iteration {int(row['Iteration'])}: Used points xₙ₋₁ = {row['xₙ₋₁']:.6f} and xₙ = {row['xₙ']:.6f} to draw secant line. Next approximation is xₙ₊₁ = {row['xₙ₊₁']:.6f}.")
print(exps)
