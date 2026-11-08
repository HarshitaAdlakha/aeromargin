You are estimating the crack-initiation life of a lower wing skin detail in flights.

**Stress history**
The stress at the detail (ksi) follows this sequence of turning points in every flight, starting and ending on the ground:

`-6, 14, 8, 19, 11, 24, 9, 21, 13, 17, 7, 16, -6`

Every flight repeats this exact sequence, one after another.

**Material and method**
- Count cycles with rainflow counting (ASTM E1049). Because the history repeats, count it as a repeating history (rearrange it to start and end at the highest peak), so every cycle is a full closed cycle and there are no half cycles.
- For each cycle: stress amplitude Sa = (Smax − Smin)/2; mean stress Sm = (Smax + Smin)/2.
- Mean-stress correction: Goodman, with Ftu = 78 ksi: Sa,eq = Sa / (1 − Sm/Ftu) when Sm > 0. When Sm ≤ 0, take Sa,eq = Sa.
- Fully reversed S-N curve: Sa,eq = 95 · N^(−0.15) (ksi; N = cycles to failure).
- Cycles with Sa,eq below 6.0 ksi cause no damage.
- Damage: Palmgren–Miner linear rule; failure when the damage sum reaches 1.0. No scatter factor.

**Report**
1. Number of rainflow cycles per flight
2. The maximum and minimum stress of the largest-range cycle
3. Damage per flight
4. Life in flights (1 ÷ damage per flight)

Show your working. End your answer with a single JSON object in a ```json code block, with exactly these keys and plain numbers:

```json
{"cycles_per_flight": 0, "largest_cycle_max_ksi": 0, "largest_cycle_min_ksi": 0, "damage_per_flight": 0, "life_flights": 0}
```
