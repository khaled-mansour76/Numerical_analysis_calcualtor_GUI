def solve(x_vals, y_vals, x_target, h=None):
    n = len(x_vals)
    if n < 2:
        raise ValueError("At least 2 data points required.")

    # Build backward difference table
    diff = [list(y_vals)]
    for order in range(1, n):
        prev = diff[order - 1]
        curr = [prev[i + 1] - prev[i] for i in range(len(prev) - 1)]
        diff.append(curr)

    xn = x_vals[-1]
    if h is None:
        h = x_vals[1] - x_vals[0]

    s = (x_target - xn) / h

    steps = []
    steps.append(f"xₙ = {xn},  h = {h},  target x = {x_target}")
    steps.append(f"s = (x - xₙ) / h = ({x_target} - {xn}) / {h} = {s}")

    # Backward difference values: ∇ky_n = diff[k][n-k-1]
    steps.append("Backward Difference Table (last-column values used):")
    for order in range(n):
        idx = n - order - 1
        if idx < len(diff[order]):
            val = diff[order][idx]
            steps.append(f"  ∇{order}yₙ = {val}")

    # Newton Backward formula: y = yn + s*∇yn + s(s+1)/2!*∇²yn + ...
    yn = diff[0][n - 1]
    result = yn
    s_product = 1.0
    factorial = 1.0

    steps.append(f"\nApplying Newton Backward Formula:")
    steps.append(f"  Term 0: yₙ = {yn}")

    for k in range(1, n):
        idx = n - k - 1
        if idx < 0 or idx >= len(diff[k]):
            break
        s_product *= (s + (k - 1))
        factorial *= k
        delta_k = diff[k][idx]
        term = s_product / factorial * delta_k
        result += term
        steps.append(
            f"  Term {k}: [s(s+1)···(s+{k-1}) / {k}!] × ∇{k}yₙ"
            f" = [{s_product:.6f} / {factorial:.0f}] × {delta_k} = {term}"
        )

    steps.append(f"\nFinal Interpolated Value at x = {x_target}:  y ≈ {result}")

    explanation = (
        "Newton Backward Interpolation is best suited when interpolating near the "
        "end of the data table. s = (x − xₙ)/h is negative for points inside the "
        "table, and the formula uses backward differences ∇ᵏyₙ read from the last "
        "column of the difference table."
    )

    return {
        "result": result,
        "steps": steps,
        "explanation": explanation,
        "diff_table": diff
    }
