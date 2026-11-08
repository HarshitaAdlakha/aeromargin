Estimate the crack-initiation life, in flights, of a lower wing skin detail.

**Stress history**
Each flight produces this sequence of turning points at the detail (ksi), ground to ground:

`-6, 14, 8, 19, 11, 24, 9, 21, 13, 17, 7, 16, -6`

Flights follow one another with the identical sequence.

**Data and practice**
- Cycle counting: rainflow (ASTM E1049), applied to the history as it repeats flight after flight, so that every counted cycle is closed.
- Mean-stress correction: Goodman with Ftu = 78 ksi, Sa,eq = Sa / (1 − Sm/Ftu) for Sm > 0; Sa,eq = Sa for Sm ≤ 0.
- Fully reversed S-N curve: Sa,eq = 95 · N^(−0.15) (ksi; N = cycles to failure). Cycles with Sa,eq below 6.0 ksi do no damage.
- Palmgren–Miner linear damage; failure at a damage sum of 1.0; no scatter factor.

**Report**
1. Rainflow cycles per flight
2. Maximum and minimum stress of the largest-range cycle
3. Damage per flight
4. Life in flights

Show your working. End with a single JSON object in a ```json code block, with exactly these keys and plain numbers:

```json
{"cycles_per_flight": 0, "largest_cycle_max_ksi": 0, "largest_cycle_min_ksi": 0, "damage_per_flight": 0, "life_flights": 0}
```
