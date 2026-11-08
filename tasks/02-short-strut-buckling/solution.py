"""Reference solution: pinned aluminium tube strut, Euler vs Johnson-parabola regime."""
import math

OD, WALL, L = 1.000, 0.065, 20.0   # in
E, FCY = 9.9e6, 35_000.0           # psi
P_LIMIT, FS = 3_100.0, 1.5         # lbf, -
C_FIX = 1.0                        # pinned-pinned, L' = L / sqrt(c)


def solve():
    idia = OD - 2 * WALL
    area = math.pi / 4 * (OD ** 2 - idia ** 2)
    inertia = math.pi / 64 * (OD ** 4 - idia ** 4)
    rho = math.sqrt(inertia / area)
    slender = (L / math.sqrt(C_FIX)) / rho
    trans = math.pi * math.sqrt(2 * E / FCY)
    if slender < trans:
        regime = "johnson"
        fcr = FCY - FCY ** 2 / (4 * math.pi ** 2 * E) * slender ** 2
    else:
        regime = "euler"
        fcr = math.pi ** 2 * E / slender ** 2
    pcr = fcr * area
    ms = pcr / (P_LIMIT * FS) - 1.0
    return {
        "slenderness_ratio": round(slender, 2),
        "transition_slenderness": round(trans, 2),
        "regime": regime,
        "critical_stress_psi": round(fcr, 0),
        "critical_load_lbf": round(pcr, 0),
        "ms": round(ms, 4),
        "verdict": "pass" if ms >= 0 else "fail",
    }


if __name__ == "__main__":
    print(solve())
