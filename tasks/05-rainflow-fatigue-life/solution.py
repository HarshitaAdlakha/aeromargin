"""Reference solution: rainflow-count one repeating flight, Goodman mean-stress correction, Miner's rule."""
import math

# Stress at a lower-wing-skin detail over one flight (ksi), ground -> flight -> ground.
HISTORY = [-6, 14, 8, 19, 11, 24, 9, 21, 13, 17, 7, 16, -6]
FTU = 78.0                  # ksi
A_SN, B_SN = 95.0, -0.15   # Sa_eq = A * N^B (ksi), fully reversed, N in cycles
S_CUTOFF = 6.0              # ksi: cycles with Sa_eq below this cause no damage


def reversals(seq):
    out = [seq[0]]
    for x in seq[1:]:
        if x == out[-1]:
            continue
        if len(out) >= 2 and (out[-1] - out[-2]) * (x - out[-1]) > 0:
            out[-1] = x
        else:
            out.append(x)
    return out


def rainflow_repeating(history):
    """Full cycles of a repeating history: rotate to start and end at the maximum peak,
    then run the ASTM E1049 three-point rule; every cycle closes."""
    h = history[:-1] if history[0] == history[-1] else history[:]
    i = max(range(len(h)), key=lambda k: h[k])
    seq = reversals(h[i:] + h[:i] + [h[i]])
    stack, cycles = [], []
    for x in seq:
        stack.append(x)
        while len(stack) >= 3:
            y = abs(stack[-2] - stack[-3])
            xr = abs(stack[-1] - stack[-2])
            if xr < y:
                break
            a, b = stack[-3], stack[-2]
            cycles.append((max(a, b), min(a, b)))
            del stack[-3:-1]
    return cycles


def sa_eq(smax, smin):
    sa, sm = (smax - smin) / 2, (smax + smin) / 2
    return sa / (1 - sm / FTU) if sm > 0 else sa


def solve():
    cycles = rainflow_repeating(HISTORY)
    dmg = 0.0
    for smax, smin in cycles:
        s = sa_eq(smax, smin)
        if s >= S_CUTOFF:
            dmg += 1.0 / (s / A_SN) ** (1 / B_SN)
    gag = max(cycles, key=lambda c: c[0] - c[1])
    return {
        "cycles_per_flight": len(cycles),
        "largest_cycle_max_ksi": gag[0],
        "largest_cycle_min_ksi": gag[1],
        "damage_per_flight": dmg,
        "life_flights": round(1 / dmg, 0),
        "_cycles": cycles,
    }


if __name__ == "__main__":
    print(solve())
