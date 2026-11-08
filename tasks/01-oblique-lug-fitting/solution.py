"""Reference solution: oblique-load lug fitting (Bruhn D1.8 interaction, Ra^1.6 + Rtr^1.6 = 1)."""
import math

P_LIMIT = 15_000.0      # lbf, limit load
ANGLE_DEG = 40.0        # load angle from the lug axis
FS = 1.5                # ultimate factor of safety
FF = 1.15               # fitting factor, applied to every check
P_AXIAL_ALLOW = 38_000.0  # lbf, lug ultimate axial allowable
P_TRANS_ALLOW = 21_000.0  # lbf, lug ultimate transverse allowable
PIN_D = 0.625           # in
PIN_FSU = 95_000.0      # psi


def solve():
    pu = P_LIMIT * FS * FF
    th = math.radians(ANGLE_DEG)
    pa, ptr = pu * math.cos(th), pu * math.sin(th)
    ra, rtr = pa / P_AXIAL_ALLOW, ptr / P_TRANS_ALLOW
    ms_lug = 1.0 / (ra ** 1.6 + rtr ** 1.6) ** (1 / 1.6) - 1.0
    pin_allow = PIN_FSU * 2 * math.pi / 4 * PIN_D ** 2   # double shear
    ms_pin = pin_allow / pu - 1.0
    gov = "lug_oblique" if ms_lug < ms_pin else "pin_shear"
    return {
        "ultimate_design_load_lbf": round(pu, 1),
        "axial_component_lbf": round(pa, 1),
        "transverse_component_lbf": round(ptr, 1),
        "ms_lug_oblique": round(ms_lug, 4),
        "ms_pin_shear": round(ms_pin, 4),
        "governing_check": gov,
        "verdict": "pass" if min(ms_lug, ms_pin) >= 0 else "fail",
    }


if __name__ == "__main__":
    print(solve())
