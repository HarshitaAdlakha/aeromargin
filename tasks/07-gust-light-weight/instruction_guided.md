You are checking the design limit load factors of a normal-category twin (14 CFR Part 23, certification basis before Amendment 23-64).

**Aircraft data**
- Wing area S = 175 ft²; mean geometric chord c = 5.4 ft
- Wing lift-curve slope a = 5.5 per radian
- Design cruising speed V_C = 190 KEAS
- Maximum weight 6,000 lb; minimum flying weight 4,200 lb
- Positive limit maneuvering load factor: 3.8
- Design maneuvering speed at maximum weight: 130 KEAS

**Conditions**
- Positive derived gust velocity at V_C: 50 ft/s (EAS), sea level, ρ₀ = 0.002377 slug/ft³, g = 32.2 ft/s²
- Use the gust load factor formula of 14 CFR 23.341 as it stood before Amendment 23-64, including its gust alleviation factor and the 498 constant for V in knots.

**Report**
1. The positive gust load factor at V_C at maximum weight
2. The positive gust load factor at V_C at minimum flying weight
3. The design positive limit load factor at each weight (the larger of the gust and maneuver values)
4. Which condition governs at minimum flying weight: `gust` or `maneuver`
5. The design maneuvering speed V_A at minimum flying weight (KEAS), scaling the maximum-weight value the standard way for a lighter aircraft

Show your working. End your answer with a single JSON object in a ```json code block, with exactly these keys and plain numbers:

```json
{"n_gust_max_weight": 0, "n_gust_min_weight": 0, "design_n_max_weight": 0, "design_n_min_weight": 0, "governing_min_weight": "gust|maneuver", "va_min_weight_keas": 0}
```
