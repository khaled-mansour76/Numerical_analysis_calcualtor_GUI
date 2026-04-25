def solve(x_vals, y_vals, y_target):
    """
    Lagrange Inverse Interpolation.

    Given tabulated (x, y) pairs, find the x value corresponding to a
    given y_target by treating the roles of x and y as swapped and
    applying the standard Lagrange formula with:

        • nodes   → y_vals  (become the "x-axis" of the interpolation)
        • values  → x_vals  (become the "y-axis" of the interpolation)
        • query   → y_target

    Result is the x such that f(x) ≈ y_target.

    This technique is valid when the y values are distinct and monotone
    (i.e. the inverse function exists and is single-valued in the range).
    """
    n = len(x_vals)
    if n < 2:
        raise ValueError("At least 2 data points required.")
    if len(y_vals) != n:
        raise ValueError("x_vals and y_vals must have the same length.")

    # Check for duplicate y values (inverse would be non-unique)
    if len(set(y_vals)) != n:
        raise ValueError(
            "y_vals contain duplicate entries — inverse interpolation "
            "requires all y values to be distinct."
        )

    steps = []
    steps.append(f"Target y = {y_target}")
    steps.append(
        "Inverse interpolation: swap roles — treat y_vals as nodes, x_vals as values."
    )
    steps.append(
        f"Nodes   (y): " + "  ".join(str(v) for v in y_vals)
    )
    steps.append(
        f"Values  (x): " + "  ".join(str(v) for v in x_vals)
    )
    steps.append("")

    result = 0.0

    for i in range(n):
        numerator   = 1.0
        denominator = 1.0
        num_parts   = []
        den_parts   = []

        for j in range(n):
            if j == i:
                continue
            numerator   *= (y_target  - y_vals[j])
            denominator *= (y_vals[i] - y_vals[j])
            num_parts.append(f"(y - {y_vals[j]})")
            den_parts.append(f"({y_vals[i]} - {y_vals[j]})")

        Li   = numerator / denominator
        term = x_vals[i] * Li
        result += term

        steps.append(
            f"L_{i}(y) = [{'·'.join(num_parts)}] / [{'·'.join(den_parts)}]"
            f"  =  {numerator} / {denominator}  =  {Li}"
        )
        steps.append(
            f"  Contribution:  x_{i} · L_{i} = {x_vals[i]} × {Li} = {term}"
        )
        steps.append("")

    steps.append(
        f"P({y_target}) = " + " + ".join(f"{x_vals[i]}·L_{i}" for i in range(n))
    )
    steps.append(f"Final Inverse-Interpolated x value:  x ≈ {result}")

    explanation = (
        "Lagrange Inverse Interpolation finds the independent variable x for a "
        "given dependent value y_target. The standard Lagrange formula is applied "
        "with the data transposed: the y column acts as the interpolation nodes "
        "and the x column provides the function values. This yields "
        "x = Σ xᵢ · Lᵢ(y_target) directly, without the need to solve a polynomial "
        "equation. The method assumes a monotone, single-valued inverse exists."
    )

    return {
        "result": result,
        "steps": steps,
        "explanation": explanation
    }
