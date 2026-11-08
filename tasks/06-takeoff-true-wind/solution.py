"""Reference solution: POH-style takeoff table, pressure altitude, METAR (true) wind vs magnetic runway, corrections."""
import math

# Short-field takeoff at 2,550 lb, flaps 10. (ground_roll_ft, total_over_50ft_ft)
PA = [0, 2000, 4000]
OAT = [0, 10, 20, 30, 40]
TABLE = {
    0:    [(860, 1465), (925, 1575), (995, 1690), (1070, 1810), (1150, 1945)],
    2000: [(1030, 1740), (1110, 1875), (1195, 2015), (1285, 2165), (1380, 2330)],
    4000: [(1235, 2085), (1335, 2255), (1440, 2440), (1550, 2640), (1670, 2865)],
}
FIELD_ELEV = 1_450.0
ALTIMETER_INHG = 29.62
OAT_C = 27.0
RUNWAY_HDG_MAG = 178.0          # runway 18
METAR_WIND_DIR, METAR_WIND_KT = 260.0, 14.0
VARIATION_DEG_EAST = 15.0       # magnetic variation 15 deg E
RUNWAY_AVAILABLE_FT = 2_500.0   # TORA after NOTAM (runway length 2,700 ft)
COMPANY_FACTOR = 1.25           # total distance x 1.25 must not exceed runway available


def lerp(x, x0, x1, y0, y1):
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def table_at(pa, oat):
    i = 0 if pa <= 2000 else 1
    j = min(int(oat // 10), 3)
    out = []
    for k in (0, 1):
        lo = lerp(oat, OAT[j], OAT[j + 1], TABLE[PA[i]][j][k], TABLE[PA[i]][j + 1][k])
        hi = lerp(oat, OAT[j], OAT[j + 1], TABLE[PA[i + 1]][j][k], TABLE[PA[i + 1]][j + 1][k])
        out.append(lerp(pa, PA[i], PA[i + 1], lo, hi))
    return out


def headwind(wind_from_true):
    wind_mag = wind_from_true - VARIATION_DEG_EAST   # east is least
    return METAR_WIND_KT * math.cos(math.radians(wind_mag - RUNWAY_HDG_MAG))


def corrected(pa, hw):
    gr, tot = table_at(pa, OAT_C)
    if hw >= 0:
        f = 1 - 0.10 * hw / 9
    else:
        f = 1 + 0.10 * (-hw) / 2
    gr, tot = gr * f, tot * f
    add = 0.15 * gr            # dry grass: + 15% of the ground roll figure, to both
    return gr + add, tot + add


def solve():
    pa = FIELD_ELEV + (29.92 - ALTIMETER_INHG) * 1000
    hw = headwind(METAR_WIND_DIR)
    gr, tot = corrected(pa, hw)
    return {
        "pressure_altitude_ft": round(pa, 0),
        "headwind_component_kt": round(hw, 2),
        "ground_roll_ft": round(gr, 0),
        "total_over_50ft_ft": round(tot, 0),
        "required_runway_ft": round(tot * COMPANY_FACTOR, 0),
        "meets_company_rule": tot * COMPANY_FACTOR <= RUNWAY_AVAILABLE_FT,
    }


if __name__ == "__main__":
    print(solve())
