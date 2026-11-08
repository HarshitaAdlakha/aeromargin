"""Reference solution: thin-walled Z-section under a moment about the horizontal centroidal axis (unsymmetric bending).
Centre-line, thin-wall model (t^3 terms dropped). Origin at the centroid (mid-web), x to the right, y up.
General bending stress with Mx only (moment about x), tension positive:
    sigma = Mx * (Iy*y - Ixy*x) / (Ix*Iy - Ixy^2)
Mx is signed so that, for a symmetric section, the top (y > 0) would be in compression."""

T = 0.10        # in
H = 3.0         # in, web between flange centre lines
B = 1.0         # in, each flange length
MOMENT = 5_000.0  # in-lb, compressing the top of the section

POINTS = {"A": (B, H / 2), "B": (0.0, H / 2), "C": (0.0, -H / 2), "D": (-B, -H / 2)}


def solve():
    ix = T * H ** 3 / 12 + 2 * (T * B * (H / 2) ** 2)
    iy = 2 * (T * B ** 3 / 12 + T * B * (B / 2) ** 2)
    ixy = (T * B) * (B / 2) * (H / 2) + (T * B) * (-B / 2) * (-H / 2)
    mx = -MOMENT
    den = ix * iy - ixy ** 2
    s = {k: mx * (iy * y - ixy * x) / den for k, (x, y) in POINTS.items()}
    return {
        "ix_in4": round(ix, 4),
        "iy_in4": round(iy, 4),
        "ixy_in4": round(ixy, 4),
        "stress_A_psi": round(s["A"], 0),
        "stress_B_psi": round(s["B"], 0),
        "stress_C_psi": round(s["C"], 0),
        "stress_D_psi": round(s["D"], 0),
        "max_abs_stress_psi": round(max(abs(v) for v in s.values()), 0),
    }


if __name__ == "__main__":
    print(solve())
