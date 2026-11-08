"""Reference solution: CAS -> Mach -> TAS at FL410, ISA+10, plus density altitude (ICAO standard atmosphere)."""
import math

P0, T0, G0, R, GAMMA = 101_325.0, 288.15, 9.80665, 287.05287, 1.4
LAPSE, H11, T11 = 0.0065, 11_000.0, 216.65
FT, KT = 0.3048, 0.514444
A0_KT = math.sqrt(GAMMA * R * T0) / KT

PA_FT, ISA_DEV, CAS_KT = 41_000.0, 10.0, 250.0


def p_isa(h):
    if h <= H11:
        return P0 * (1 - LAPSE * h / T0) ** (G0 / (R * LAPSE))
    p11 = p_isa(H11)
    return p11 * math.exp(-G0 * (h - H11) / (R * T11))


def t_isa(h):
    return T0 - LAPSE * h if h <= H11 else T11


def rho_isa(h):
    return p_isa(h) / (R * t_isa(h))


def density_altitude(rho):
    lo, hi = -2000.0, 25_000.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if rho_isa(mid) > rho:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def solve():
    h = PA_FT * FT
    p = p_isa(h)
    oat = t_isa(h) + ISA_DEV
    qc = P0 * ((1 + 0.2 * (CAS_KT / A0_KT) ** 2) ** 3.5 - 1)
    mach = math.sqrt(5 * ((qc / p + 1) ** (2 / 7) - 1))
    tas = mach * math.sqrt(GAMMA * R * oat) / KT
    rho = p / (R * oat)
    return {
        "static_pressure_pa": round(p, 0),
        "oat_k": round(oat, 2),
        "mach": round(mach, 4),
        "tas_kt": round(tas, 1),
        "density_altitude_ft": round(density_altitude(rho) / FT, 0),
    }


if __name__ == "__main__":
    print(solve())
