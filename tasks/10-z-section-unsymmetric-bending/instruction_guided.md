Stress check request: a cabin floor beam with a thin-walled Z cross-section.

**Section** (uniform thickness 0.10 in; use centre-line dimensions and the thin-wall approximation, dropping terms in t³)
- Web: vertical, 3.0 in between the flange centre lines
- Top flange: 1.0 in long, extending horizontally to the RIGHT from the top of the web
- Bottom flange: 1.0 in long, extending horizontally to the LEFT from the bottom of the web

Points on the section: A = free tip of the top flange; B = top web–flange corner; C = bottom web–flange corner; D = free tip of the bottom flange.

**Loading**
The beam is loaded vertically and has no lateral restraint. At the section checked, the bending moment is 5,000 in·lb about the horizontal axis through the centroid, in the sense that compresses the top of the section.

**Method**
A Z-section is unsymmetric: its product of inertia about the centroidal x–y axes is not zero, so the simple formula σ = My/I does not apply. Use the general unsymmetric bending formula with Ix, Iy and Ixy (the neutral axis is not horizontal).

**Report** (bending stresses in psi, tension positive, compression negative)
1. The section's second moments of area about the horizontal and vertical centroidal axes, and the product of inertia (in⁴; sign of the product of inertia with x to the right and y up)
2. The bending stress at A, B, C and D
3. The largest magnitude of bending stress on the section

Show your working. End with a single JSON object in a ```json code block, with exactly these keys and plain numbers:

```json
{"ix_in4": 0, "iy_in4": 0, "ixy_in4": 0, "stress_A_psi": 0, "stress_B_psi": 0, "stress_C_psi": 0, "stress_D_psi": 0, "max_abs_stress_psi": 0}
```
