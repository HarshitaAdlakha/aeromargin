A student pilot asks you, their instructor, to check this morning's takeoff planning. The aircraft is a single-engine piston at 2,550 lb; short-field technique, flaps 10°.

**Takeoff distance table (flight manual), feet: ground roll / total over a 50 ft obstacle**

| Pressure altitude | 0 °C | 10 °C | 20 °C | 30 °C | 40 °C |
|---|---|---|---|---|---|
| Sea level | 860 / 1465 | 925 / 1575 | 995 / 1690 | 1070 / 1810 | 1150 / 1945 |
| 2000 ft | 1030 / 1740 | 1110 / 1875 | 1195 / 2015 | 1285 / 2165 | 1380 / 2330 |
| 4000 ft | 1235 / 2085 | 1335 / 2255 | 1440 / 2440 | 1550 / 2640 | 1670 / 2865 |

Flight manual notes:
1. Decrease distances 10% for each 9 knots headwind. For operation with tailwinds up to 10 knots, increase distances by 10% for each 2 knots. (Apply proportionally.)
2. For operation on a dry, grass runway, increase distances by 15% of the "ground roll" figure (add that amount to both figures).
3. Apply the wind correction first, then the surface correction. Interpolate the table linearly.

**Airfield data (from the chart supplement)**
Elevation 1,450 ft. Magnetic variation 15° E. Runway 18/36, dry grass, 2,700 ft. Runway 18 magnetic heading 178°.

**NOTAM**
RWY 18 TORA 2,500 FT. FIRST 200 FT RWY 18 CLSD WIP.

**Weather**
METAR: `27/12 A2962`, wind `26014KT`, no gusts, visibility and cloud not limiting.

**School rule**
Total distance over 50 ft × 1.25 must not exceed the take-off run available.

**Report**
1. Pressure altitude (ft)
2. Headwind component on the departure runway (kt; negative for a tailwind)
3. Corrected ground roll and corrected total distance over 50 ft (ft)
4. Runway required under the school rule (ft)
5. Whether the takeoff meets the school rule (true/false)

Show your working. End with a single JSON object in a ```json code block, with exactly these keys, plain numbers and a JSON boolean:

```json
{"pressure_altitude_ft": 0, "headwind_component_kt": 0, "ground_roll_ft": 0, "total_over_50ft_ft": 0, "required_runway_ft": 0, "meets_company_rule": true}
```
