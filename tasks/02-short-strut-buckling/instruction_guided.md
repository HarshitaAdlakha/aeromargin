You are sizing a compression strut in a light aircraft's landing-gear bay.

**Strut**
- Round aluminium tube: outside diameter 1.000 in, wall thickness 0.065 in
- Length between pin centres: 20.0 in. Both ends are pinned (end-fixity coefficient c = 1, so the effective length L′ = L/√c = 20.0 in).
- Material properties: E = 9.9 × 10⁶ psi; compressive yield stress Fcy = 35,000 psi
- Local crippling of the tube wall does not govern; ignore it.

**Loading**
- Limit axial compression: 3,100 lbf. Ultimate factor of safety: 1.5. No fitting factor.

**Method**
Use the classical column method of Bruhn, Section C2: the Euler hyperbola for long columns and the Johnson parabola (with Fcy as the cut-off stress) for short columns. Use the slenderness ratio at which the two curves are tangent to decide which one applies.

**Report**
1. The slenderness ratio L′/ρ (ρ = radius of gyration)
2. The transition (tangency) slenderness ratio
3. Which curve applies: `johnson` or `euler`
4. The critical buckling stress (psi) and critical load (lbf)
5. The margin of safety at ultimate load, MS = P_cr / P_ult − 1
6. The verdict: `pass` if MS ≥ 0, otherwise `fail`

Show your working. End your answer with a single JSON object in a ```json code block, with exactly these keys and plain numbers:

```json
{"slenderness_ratio": 0, "transition_slenderness": 0, "regime": "johnson|euler", "critical_stress_psi": 0, "critical_load_lbf": 0, "ms": 0, "verdict": "pass|fail"}
```
