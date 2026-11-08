Stress check request: a bracket bolted to a frame, loaded in its own plane by an eccentric shear load.

**Bolts** (x to the right from the left bolt column, y up from the middle row; all in single shear)

| Bolt | x (in) | y (in) | Diameter (in) |
|---|---|---|---|
| L1 | 0.0 | +2.5 | 0.250 |
| L2 | 0.0 | 0.0 | 0.250 |
| L3 | 0.0 | −2.5 | 0.250 |
| R1 | 3.0 | +2.5 | 0.1875 |
| R2 | 3.0 | 0.0 | 0.1875 |
| R3 | 3.0 | −2.5 | 0.1875 |

All bolts are the same steel, ultimate shear strength 95,000 psi on the full-diameter area (allowable = 95,000 × πd²/4). Bearing and the bracket do not govern.

**Load**
Ultimate 4,200 lbf, straight down (−y), line of action at x = 9.0 in.

**Scope**
Use the elastic method for an eccentrically loaded fastener group (Bruhn, Section D1), taking each bolt's shear stiffness as proportional to its shear area.

**Report**
1. The x-coordinate of the fastener group's centroid (in)
2. The load's eccentricity from that centroid (in)
3. The critical bolt (lowest margin of safety), its resultant load (lbf) and its margin, MS = allowable/load − 1
4. The verdict: `pass` if every bolt has MS ≥ 0, otherwise `fail`

Show your working. End with a single JSON object in a ```json code block, with exactly these keys and plain numbers (bolt by name, e.g. "L2"; if two bolts tie, give either):

```json
{"centroid_x_in": 0, "eccentricity_in": 0, "critical_bolt": "L1", "critical_bolt_load_lbf": 0, "min_ms": 0, "verdict": "pass|fail"}
```
