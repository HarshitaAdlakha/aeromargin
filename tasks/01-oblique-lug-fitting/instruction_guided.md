You are checking a single-lug fitting on a transport-category aircraft (14 CFR Part 25).

**Geometry and loading**
- A steel pin of diameter 0.625 in passes through a single aluminium lug, which sits between the two plates of a clevis. The pin is therefore in double shear.
- Limit load on the fitting: 15,000 lbf, acting in the plane of the lug at 40° from the lug's axis (the axis runs from the pin centre to the lug's attachment).
- Ultimate factor of safety: 1.5.
- Fitting factor: 1.15. Apply it to every check in this task, the pin included.

**Allowables (ultimate)**
- Lug, pure axial load (lowest of shear-bearing and net-tension, already read from the design charts): 38,000 lbf
- Lug, pure transverse load (already read from the design charts): 21,000 lbf
- Pin ultimate shear strength: 95,000 psi

**Method**
- Analyse the lug for the oblique load with the oblique-load interaction curve used in Bruhn's lug analysis (Analysis and Design of Flight Vehicle Structures, Section D1.8), using the ultimate allowables above.
- Check the pin in shear only (pin bending is outside this task).
- Margin of safety: MS = (allowable / applied) − 1. For the lug, use the MS defined by that interaction curve.

**Report**
1. The ultimate design load (limit × factor of safety × fitting factor), in lbf
2. Its axial and transverse components, in lbf
3. The lug MS under the oblique load
4. The pin shear MS
5. Which check governs: `lug_oblique` or `pin_shear`
6. The verdict: `pass` if every MS ≥ 0, otherwise `fail`

Show your working. End your answer with a single JSON object in a ```json code block, with exactly these keys and plain numbers (no units in the values):

```json
{"ultimate_design_load_lbf": 0, "axial_component_lbf": 0, "transverse_component_lbf": 0, "ms_lug_oblique": 0, "ms_pin_shear": 0, "governing_check": "lug_oblique|pin_shear", "verdict": "pass|fail"}
```
