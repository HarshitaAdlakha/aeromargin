"""Reference solution: eccentric in-plane shear on a bolt group with two bolt sizes (elastic method,
bolt stiffness proportional to shear area: area-weighted centroid and polar moment)."""
import math

FSU = 95_000.0                    # psi, bolt ultimate shear strength (single shear)
D_LEFT, D_RIGHT = 0.250, 0.1875   # in
# (name, x, y, diameter); x measured from the left bolt column, y from the middle row
BOLTS = [
    ("L1", 0.0, 2.5, D_LEFT), ("L2", 0.0, 0.0, D_LEFT), ("L3", 0.0, -2.5, D_LEFT),
    ("R1", 3.0, 2.5, D_RIGHT), ("R2", 3.0, 0.0, D_RIGHT), ("R3", 3.0, -2.5, D_RIGHT),
]
P_ULT = 4_200.0       # lbf, ultimate, acting straight down (-y)
X_LOAD = 9.0          # in, line of action measured from the left bolt column


def solve():
    areas = [math.pi / 4 * d ** 2 for *_, d in BOLTS]
    a_tot = sum(areas)
    xc = sum(a * b[1] for a, b in zip(areas, BOLTS)) / a_tot
    yc = sum(a * b[2] for a, b in zip(areas, BOLTS)) / a_tot
    j = sum(a * ((b[1] - xc) ** 2 + (b[2] - yc) ** 2) for a, b in zip(areas, BOLTS))
    torque = -P_ULT * (X_LOAD - xc)           # load down, to the right of centroid: clockwise (negative)
    res = []
    for a, (name, x, y, d) in zip(areas, BOLTS):
        dx, dy = x - xc, y - yc
        fx = a * (-torque * dy / j)            # reaction resists the applied moment
        fy = a * (P_ULT / a_tot + torque * dx / j * -1)
        f = math.hypot(fx, fy)
        allow = FSU * a
        res.append((allow / f - 1, name, f))
    res.sort()
    ms, name, f = res[0]
    return {
        "centroid_x_in": round(xc, 4),
        "eccentricity_in": round(X_LOAD - xc, 4),
        "critical_bolt": name,
        "critical_bolt_load_lbf": round(f, 1),
        "min_ms": round(ms, 4),
        "verdict": "pass" if ms >= 0 else "fail",
        "_all": [(n, round(F, 1), round(m, 4)) for m, n, F in res],
    }


if __name__ == "__main__":
    print(solve())
