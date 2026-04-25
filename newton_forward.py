def solve(x_vals, y_vals, x_target, h=None):
    n = len(x_vals)
    if n < 2:
        raise ValueError("At least 2 data points required.")

    # Build forward difference table
    diff = [list(y_vals)]
    for order in range(1, n):
        prev = diff[order - 1]
        curr = [prev[i + 1] - prev[i] for i in range(len(prev) - 1)]
        diff.append(curr)

    x0 = x_vals[0]
    if h is None:
        h = x_vals[1] - x_vals[0]

    s = (x_target - x0) / h

    steps = []
    steps.append(f"x₀ = {x0},  h = {h},  target x = {x_target}")
    steps.append(f"s = (x - x₀) / h = ({x_target} - {x0}) / {h} = {s}")

    # Build difference table step info
    steps.append("Forward Difference Table:")
    for order in range(n):
        row_vals = "  ".join(str(v) for v in diff[order])
        steps.append(f"  Δ{'⁰¹²³⁴⁵⁶⁷⁸⁹'[order] if order < 10 else order}y: {row_vals}")

    # Newton Forward formula: y = y0 + s*Δy0 + s(s-1)/2! * Δ²y0 + ...
    result = diff[0][0]
    s_product = 1.0
    factorial = 1.0
    term_val = diff[0][0]

    steps.append(f"\nApplying Newton Forward Formula:")
    steps.append(f"  Term 0: y₀ = {diff[0][0]}")

    for k in range(1, n):
        if k > len(diff) - 1 or len(diff[k]) == 0:
            break
        s_product *= (s - (k - 1))
        factorial *= k
        delta_k = diff[k][0]
        term = s_product / factorial * delta_k
        result += term
        steps.append(
            f"  Term {k}: [s(s-1)···(s-{k-1}) / {k}!] × Δ{k}y₀"
            f" = [{s_product:.6f} / {factorial:.0f}] × {delta_k} = {term}"
        )

    steps.append(f"\nFinal Interpolated Value at x = {x_target}:  y ≈ {result}")

    explanation = (
        "Newton Forward Interpolation uses a table of forward finite differences "
        "built from equispaced data. The parameter s = (x − x₀)/h maps the target "
        "into the normalized space, and the Gregory-Newton formula accumulates "
        "difference terms up to order n−1 to give the interpolated value."
    )

    return {
        "result": result,
        "steps": steps,
        "explanation": explanation,
        "diff_table": diff
    }
