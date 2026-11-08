"""Reference solution: 14 CFR 23.341 (pre-Amdt 23-64) gust load factor at two weights, and VA at light weight."""
import math

S, CBAR, A_SLOPE = 175.0, 5.4, 5.5      # ft^2, ft, per rad
VC, UDE = 190.0, 50.0                    # KEAS, ft/s
RHO0, G = 0.002377, 32.2                 # slug/ft^3, ft/s^2
W_MAX, W_MIN = 6_000.0, 4_200.0          # lb
N_MANEUVER = 3.8
VA_AT_WMAX = 130.0                       # KEAS


def gust_n(w):
    ws = w / S
    mu = 2 * ws / (RHO0 * CBAR * A_SLOPE * G)
    kg = 0.88 * mu / (5.3 + mu)
    return 1 + kg * UDE * VC * A_SLOPE / (498 * ws)


def solve():
    nh, nl = gust_n(W_MAX), gust_n(W_MIN)
    return {
        "n_gust_max_weight": round(nh, 3),
        "n_gust_min_weight": round(nl, 3),
        "design_n_max_weight": round(max(nh, N_MANEUVER), 3),
        "design_n_min_weight": round(max(nl, N_MANEUVER), 3),
        "governing_min_weight": "gust" if nl > N_MANEUVER else "maneuver",
        "va_min_weight_keas": round(VA_AT_WMAX * math.sqrt(W_MIN / W_MAX), 1),
    }


if __name__ == "__main__":
    print(solve())
