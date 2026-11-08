Stress check request: a cantilevered support beam for a main-landing-gear side brace. The beam is an I-section built from two flanges and a stiffened shear web. It is fixed at its inboard end and carries the brace load near its outboard (free) end, where it is DEEPER than at the root: going outboard, the upper flange rises and the lower flange falls, each at a slope of 0.03 (tan α) relative to the beam's reference axis.

At the station being checked, the ultimate internal loads are:
- Shear: the loads outboard of the station add up to 6,000 lbf upward.
- Bending moment: 180,000 in·lb, putting the upper flange in compression and the lower flange in tension.

Distance between flange centroids at this station: 6.0 in. Web thickness: 0.040 in. Assume the flanges carry all the bending and the web carries a uniform shear stress over the 6.0 in depth. Web ultimate shear allowable Fsu = 30,000 psi (stiffened web; no buckling).

**Report**
1. The shear force carried by the web at this station (lbf)
2. The web shear stress (psi)
3. The margin of safety, MS = Fsu / stress − 1
4. The verdict: `pass` if MS ≥ 0, otherwise `fail`

Show your working. End with a single JSON object in a ```json code block, with exactly these keys and plain numbers:

```json
{"web_shear_lbf": 0, "web_tau_psi": 0, "ms": 0, "verdict": "pass|fail"}
```
