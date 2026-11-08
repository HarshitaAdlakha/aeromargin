Stress check request: compression strut in a light aircraft's landing-gear bay.

**Strut**
- Round aluminium tube, 1.000 in outside diameter, 0.065 in wall
- 20.0 in between pin centres; pinned at both ends (end-fixity coefficient c = 1)
- E = 9.9 × 10⁶ psi; compressive yield stress Fcy = 35,000 psi
- Local crippling of the tube wall does not govern.

**Load**
Limit axial compression 3,100 lbf. Factor of safety 1.5; no fitting factor.

**Scope**
Check the strut for primary column buckling with the classical column curves the company stress manual uses (Bruhn, Section C2), with Fcy as the material cut-off.

**Report**
1. The slenderness ratio L′/ρ
2. The slenderness ratio that separates the short-column and long-column curves
3. Which curve applies: `johnson` or `euler`
4. The critical stress (psi) and critical load (lbf)
5. The margin of safety at ultimate load, MS = P_cr/P_ult − 1
6. The verdict: `pass` if MS ≥ 0, otherwise `fail`

Show your working. End with a single JSON object in a ```json code block, with exactly these keys and plain numbers:

```json
{"slenderness_ratio": 0, "transition_slenderness": 0, "regime": "johnson|euler", "critical_stress_psi": 0, "critical_load_lbf": 0, "ms": 0, "verdict": "pass|fail"}
```
