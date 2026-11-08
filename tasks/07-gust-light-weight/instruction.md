Loads check for a normal-category twin certified to 14 CFR Part 23 before Amendment 23-64.

**Aircraft data**
- Wing area 175 ft²; mean geometric chord 5.4 ft; wing lift-curve slope 5.5 per radian
- Design cruising speed V_C = 190 KEAS
- Maximum weight 6,000 lb; minimum flying weight 4,200 lb
- Positive limit maneuvering load factor 3.8
- Design maneuvering speed at maximum weight: 130 KEAS

**Conditions**
Positive gust of 50 ft/s (EAS) at V_C, sea level (ρ₀ = 0.002377 slug/ft³, g = 32.2 ft/s²), using the 14 CFR 23.341 gust load factor formula of that certification basis.

**Report**
1. Positive gust load factor at V_C, maximum weight
2. Positive gust load factor at V_C, minimum flying weight
3. Design positive limit load factor at each weight (the larger of gust and maneuver)
4. What governs at minimum flying weight: `gust` or `maneuver`
5. Design maneuvering speed V_A at minimum flying weight (KEAS)

Show your working. End with a single JSON object in a ```json code block, with exactly these keys and plain numbers:

```json
{"n_gust_max_weight": 0, "n_gust_min_weight": 0, "design_n_max_weight": 0, "design_n_min_weight": 0, "governing_min_weight": "gust|maneuver", "va_min_weight_keas": 0}
```
