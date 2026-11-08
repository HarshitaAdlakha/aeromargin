"""Reference solution: business-jet loading, %MAC at ramp/takeoff/landing with a variable fuel arm."""

FUEL_DENSITY = 6.75          # lb per US gal (Jet-A, as stated)
LEMAC, MAC = 288.0, 80.0     # in
FWD_LIMIT, AFT_LIMIT = 15.0, 32.0   # %MAC, all weights
MTOW, MLW = 16_600.0, 15_200.0

ITEMS = [  # (weight lb, arm in)
    (9_850.0, 312.4),   # basic empty weight
    (2 * 190.0, 128.0), # crew
    (4 * 185.0, 335.0), # passengers, club seats
    (2 * 185.0, 372.0), # passengers, aft bench
    (350.0, 455.0),     # aft baggage
]
# Fuel moment table: US gal -> moment / 1000 (in-lb), at 6.75 lb/gal
FUEL_TABLE = [(0, 0.0), (100, 214.7), (200, 426.6), (300, 634.8), (400, 839.7),
              (500, 1041.2), (600, 1239.3), (700, 1436.4)]
RAMP_FUEL_GAL = 660.0
TAXI_FUEL_LB = 200.0
TRIP_FUEL_LB = 2_600.0


def fuel_moment(gal):
    for (g0, m0), (g1, m1) in zip(FUEL_TABLE, FUEL_TABLE[1:]):
        if g0 <= gal <= g1:
            return 1000 * (m0 + (m1 - m0) * (gal - g0) / (g1 - g0))
    raise ValueError(gal)


def state(fuel_lb):
    w = sum(i[0] for i in ITEMS) + fuel_lb
    m = sum(i[0] * i[1] for i in ITEMS) + fuel_moment(fuel_lb / FUEL_DENSITY)
    cg = m / w
    return w, (cg - LEMAC) / MAC * 100


def solve():
    ramp_fuel = RAMP_FUEL_GAL * FUEL_DENSITY
    to_fuel = ramp_fuel - TAXI_FUEL_LB
    ldg_fuel = to_fuel - TRIP_FUEL_LB
    wt, cgt = state(to_fuel)
    wl, cgl = state(ldg_fuel)
    to_ok = wt <= MTOW and FWD_LIMIT <= cgt <= AFT_LIMIT
    ld_ok = wl <= MLW and FWD_LIMIT <= cgl <= AFT_LIMIT
    return {
        "takeoff_weight_lb": round(wt, 0),
        "takeoff_cg_pct_mac": round(cgt, 2),
        "landing_weight_lb": round(wl, 0),
        "landing_cg_pct_mac": round(cgl, 2),
        "takeoff_within_limits": to_ok,
        "landing_within_limits": ld_ok,
    }


if __name__ == "__main__":
    print(solve())
