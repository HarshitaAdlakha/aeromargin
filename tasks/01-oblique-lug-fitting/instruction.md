Stress check request, transport-category aircraft (14 CFR Part 25). Please substantiate this fitting.

**Fitting**
- Single aluminium lug, pinned between the two plates of a steel clevis (the pin is in double shear). Pin: steel, 0.625 in diameter, ultimate shear strength 95,000 psi.
- Limit load: 15,000 lbf, in the plane of the lug, at 40° to the lug axis (the axis from the pin centre towards the lug's attachment).
- Factor of safety 1.5. Fitting factor 1.15 (14 CFR 25.625), applied to the lug and to the pin.

**Lug allowables (ultimate, already read from the design charts for this geometry and material)**
- Axial load, shear-bearing (shear-out) failure: 38,000 lbf
- Axial load, net-section tension failure: 44,000 lbf
- Transverse load: 21,000 lbf

**Scope**
Analyse the lug for this load following standard lug analysis practice (the company stress manual follows Bruhn, *Analysis and Design of Flight Vehicle Structures*, Section D1). Check the pin in shear only; pin bending is covered elsewhere. Margins of safety are written MS = (allowable/applied) − 1, or the equivalent for the method you use.

**Report**
1. The ultimate design load, in lbf, and its axial and transverse components
2. The lug's margin of safety for this load
3. The pin's shear margin of safety
4. Which check governs: `lug_oblique` (the lug under this load) or `pin_shear`
5. The verdict: `pass` if every margin is ≥ 0, otherwise `fail`

Show your working. End with a single JSON object in a ```json code block, with exactly these keys and plain numbers (no units in the values):

```json
{"ultimate_design_load_lbf": 0, "axial_component_lbf": 0, "transverse_component_lbf": 0, "ms_lug_oblique": 0, "ms_pin_shear": 0, "governing_check": "lug_oblique|pin_shear", "verdict": "pass|fail"}
```
