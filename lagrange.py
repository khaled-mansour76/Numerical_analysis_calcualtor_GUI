def solve(x_vals, y_vals, x_target):
    """
    Lagrange Interpolation.

    For n data points (x₀,y₀),…,(xₙ₋₁,yₙ₋₁) the interpolated value at
    x_target is:

        P(x) = Σᵢ yᵢ · Lᵢ(x)

    where the Lagrange basis polynomial is:

        Lᵢ(x) = Π_{j≠i} (x - xⱼ) / (xᵢ - xⱼ)
    """
    n = len(x_vals)
    if n < 2:
        raise ValueError("At least 2 data points required.")
    if len(y_vals) != n:
        raise ValueError("x_vals and y_vals must have the same length.")

    steps = []
    steps.append(f"Target x = {x_target}")
    steps.append(f"Data points: " + "  ".join(f"({x_vals[i]}, {y_vals[i]})" for i in range(n)))
    steps.append("")

    result = 0.0
    L_vals = []

    for i in range(n):
        numerator   = 1.0
        denominator = 1.0
        num_parts   = []
        den_parts   = []

        for j in range(n):
            if j == i:
                continue
            numerator   *= (x_target - x_vals[j])
            denominator *= (x_vals[i] - x_vals[j])
            num_parts.append(f"(x - {x_vals[j]})")
            den_parts.append(f"({x_vals[i]} - {x_vals[j]})")

        Li    = numerator / denominator
        term  = y_vals[i] * Li
        result += term
        L_vals.append(Li)

        steps.append(
            f"L_{i}(x) = [{'·'.join(num_parts)}] / [{'·'.join(den_parts)}]"
            f"  =  {numerator} / {denominator}  =  {Li}"
        )
        steps.append(f"  Contribution:  y_{i} · L_{i} = {y_vals[i]} × {Li} = {term}")
        steps.append("")

    steps.append(f"P({x_target}) = " + " + ".join(f"{y_vals[i]}·L_{i}" for i in range(n)))
    steps.append(f"Final Interpolated Value:  P({x_target}) ≈ {result}")

    explanation = (
        "Lagrange Interpolation constructs a unique polynomial of degree n−1 that "
        "passes through all n data points. Each basis polynomial Lᵢ(x) equals 1 "
        "at xᵢ and 0 at every other node, so the weighted sum Σ yᵢLᵢ(x) reproduces "
        "all given values exactly. No equally-spaced nodes are required."
    )

    return {
        "result": result,
        "steps": steps,
        "explanation": explanation
    }
