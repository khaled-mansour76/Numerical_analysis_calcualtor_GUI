def solve(x_vals, y_vals, x_target, h=None):
    """
    Stirling's Central Difference Interpolation Formula.

    Best used when x_target lies near the centre of the data table.
    Requires an ODD number of equally spaced points so there is a true
    central row.  If n is even the nearest-middle index is used.

    Formula (with s = (x - x₀)/h, x₀ = central point):
        y ≈ y₀
            + s * (Δy₋₁ + Δy₀)/2                          [1st mean diff]
            + s²/2! * Δ²y₋₁                               [2nd diff]
            + s(s²-1)/3! * (Δ³y₋₂ + Δ³y₋₁)/2             [3rd mean diff]
            + s²(s²-1)/4! * Δ⁴y₋₂                         [4th diff]
            + …
    """
    n = len(x_vals)
    if n < 3:
        raise ValueError("Stirling interpolation needs at least 3 data points.")

    if h is None:
        h = x_vals[1] - x_vals[0]

    # ── Build full central difference table ────────────────────────────────
    # diff[k] holds the k-th order differences (length n-k)
    diff = [list(y_vals)]
    for order in range(1, n):
        prev = diff[order - 1]
        curr = [prev[i + 1] - prev[i] for i in range(len(prev) - 1)]
        diff.append(curr)

    # ── Central index (origin x₀) ────────────────────────────────────────
    mid = (n - 1) // 2          # index of x₀ in the original array
    x0  = x_vals[mid]
    s   = (x_target - x0) / h

    steps = []
    steps.append(f"Central point  x₀ = {x0}  (index {mid}),  h = {h}")
    steps.append(f"s = (x − x₀) / h = ({x_target} − {x0}) / {h} = {s}")

    # Helper: safely fetch diff[order][index], return 0 if out of range
    def D(order, idx):
        if order >= len(diff) or idx < 0 or idx >= len(diff[order]):
            return 0.0
        return diff[order][idx]

    # ── Central difference values centred on mid ──────────────────────────
    # Notation:  Δ^k y_{mid - k//2}  is the "central" k-th difference
    steps.append("\nCentral Difference Table (values used):")
    for k in range(n):
        idx = mid - k // 2
        val = D(k, idx)
        steps.append(f"  Δ{k}y (index {idx}) = {val}")

    # ── Stirling accumulation ─────────────────────────────────────────────
    result = D(0, mid)
    steps.append(f"\nApplying Stirling's Formula:")
    steps.append(f"  Term 0 (y₀) = {result}")

    # Pre-compute factorial helper
    def fact(k):
        f = 1
        for i in range(2, k + 1):
            f *= i
        return f

    # Term 1: s * mean(Δy₋₁, Δy₀)  — odd order 1
    d1_neg = D(1, mid - 1)
    d1_pos = D(1, mid)
    mean1  = (d1_neg + d1_pos) / 2.0
    t1     = s * mean1
    result += t1
    steps.append(f"  Term 1: s × (Δ¹y₋₁ + Δ¹y₀)/2 = {s} × ({d1_neg} + {d1_pos})/2 = {t1}")

    # Term 2: (s²/2!) * Δ²y₋₁
    d2 = D(2, mid - 1)
    t2 = (s ** 2) / fact(2) * d2
    result += t2
    steps.append(f"  Term 2: (s²/2!) × Δ²y₋₁ = ({s**2:.6f}/2) × {d2} = {t2}")

    if n >= 4:
        # Term 3: s(s²-1)/3! * mean(Δ³y₋₂, Δ³y₋₁)
        d3_neg = D(3, mid - 2)
        d3_pos = D(3, mid - 1)
        mean3  = (d3_neg + d3_pos) / 2.0
        t3     = s * (s ** 2 - 1) / fact(3) * mean3
        result += t3
        steps.append(
            f"  Term 3: s(s²-1)/3! × (Δ³y₋₂+Δ³y₋₁)/2"
            f" = {s}×({s**2-1:.6f})/6 × {mean3:.6f} = {t3}"
        )

    if n >= 5:
        # Term 4: s²(s²-1)/4! * Δ⁴y₋₂
        d4 = D(4, mid - 2)
        t4 = (s ** 2) * (s ** 2 - 1) / fact(4) * d4
        result += t4
        steps.append(
            f"  Term 4: s²(s²-1)/4! × Δ⁴y₋₂"
            f" = {s**2:.6f}×{s**2-1:.6f}/24 × {d4} = {t4}"
        )

    if n >= 6:
        # Term 5: s(s²-1)(s²-4)/5! * mean(Δ⁵y₋₃, Δ⁵y₋₂)
        d5_neg = D(5, mid - 3)
        d5_pos = D(5, mid - 2)
        mean5  = (d5_neg + d5_pos) / 2.0
        t5     = s * (s ** 2 - 1) * (s ** 2 - 4) / fact(5) * mean5
        result += t5
        steps.append(
            f"  Term 5: s(s²-1)(s²-4)/5! × mean Δ⁵ = {t5}"
        )

    steps.append(f"\nFinal Interpolated Value at x = {x_target}:  y ≈ {result}")

    explanation = (
        "Stirling's formula is a central-difference interpolation scheme that "
        "averages forward and backward differences to achieve higher accuracy "
        "when the target lies near the middle of the data table. It alternates "
        "between mean differences (odd terms) and single central differences "
        "(even terms), converging faster than one-sided Newton formulas for "
        "central positions."
    )

    return {
        "result": result,
        "steps": steps,
        "explanation": explanation,
        "diff_table": diff
    }
