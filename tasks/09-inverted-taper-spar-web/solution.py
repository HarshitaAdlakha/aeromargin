"""Reference solution: web shear in a tapered beam (Resal effect) when the depth INCREASES toward the free end.

Free body = the outboard portion (from the checked station to the free end). x points outboard, z up.
  External load on the outboard portion: V upward.
  Upper flange, compression M/h (horizontal component): pushes the outboard portion OUTBOARD along the
    upper flange, which RISES going outboard  -> vertical component +(M/h)*tan(a), upward.
  Lower flange, tension M/h: pulls the outboard portion INBOARD along the lower flange, which FALLS going
    outboard (so rises going inboard)          -> vertical component +(M/h)*tan(a), upward.
Vertical equilibrium: V + 2(M/h)tan(a) + (web shear on the portion) = 0, so the web carries V + 2(M/h)tan(a).
The textbook reduction V - (M/h)(tan a1 + tan a2) applies when the depth DEcreases toward the free end
(i.e. the depth grows in the direction of increasing moment). Here it is the other way round (Megson,
Aircraft Structures, tapered beams; Bruhn, Section A11)."""

V = 6_000.0        # lbf, net external load on the outboard portion, upward
M = 180_000.0      # in-lb at the station; upper flange compression, lower flange tension
H = 6.0            # in, between flange centroids at the station
SLOPE = 0.03       # tan(a) of each flange relative to the beam axis; depth grows outboard
T_WEB = 0.040      # in
FSU = 30_000.0     # psi


def solve():
    flanges = 2 * (M / H) * SLOPE          # both vertical components act upward, with V
    v_web = V + flanges
    tau = v_web / (H * T_WEB)
    ms = FSU / tau - 1
    return {
        "flange_vertical_components_lbf": round(flanges, 1),
        "web_shear_lbf": round(v_web, 1),
        "web_tau_psi": round(tau, 0),
        "ms": round(ms, 4),
        "verdict": "pass" if ms >= 0 else "fail",
    }


if __name__ == "__main__":
    print(solve())
