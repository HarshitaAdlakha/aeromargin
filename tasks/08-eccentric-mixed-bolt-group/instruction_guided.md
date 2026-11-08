You are checking a bolted bracket loaded in its own plane by an eccentric shear load.

**Bolt pattern** (x measured to the right from the left bolt column, y measured up from the middle row; all bolts in single shear)

| Bolt | x (in) | y (in) | Diameter (in) |
|---|---|---|---|
| L1 | 0.0 | +2.5 | 0.250 |
| L2 | 0.0 | 0.0 | 0.250 |
| L3 | 0.0 | −2.5 | 0.250 |
| R1 | 3.0 | +2.5 | 0.1875 |
| R2 | 3.0 | 0.0 | 0.1875 |
| R3 | 3.0 | −2.5 | 0.1875 |

- Bolt ultimate shear strength: 95,000 psi, on the full-diameter shear area. Bolt shear allowable = 95,000 × πd²/4.
- Bearing and the bracket itself do not govern; ignore them.

**Load**
- Ultimate load: 4,200 lbf acting straight down (−y), with its line of action at x = 9.0 in.

**Method**
Use the elastic method for an eccentrically loaded bolt group. The bolts have different sizes: treat each bolt's shear stiffness as proportional to its shear area, and apply that consistently to the group centroid, the polar moment, and the distribution of both the direct and the moment-induced loads. Combine the direct and moment-induced components on each bolt as vectors.

**Report**
1. The x-coordinate of the bolt group's centroid (in)
2. The eccentricity of the load from that centroid (in)
3. The critical bolt (the one with the lowest margin of safety), its resultant load (lbf), and its margin of safety, MS = allowable / load − 1
4. The verdict: `pass` if every bolt has MS ≥ 0, otherwise `fail`

Show your working. End your answer with a single JSON object in a ```json code block, with exactly these keys and plain numbers (the critical bolt as its name, e.g. "L2"; if two bolts tie, give either):

```json
{"centroid_x_in": 0, "eccentricity_in": 0, "critical_bolt": "L1", "critical_bolt_load_lbf": 0, "min_ms": 0, "verdict": "pass|fail"}
```
