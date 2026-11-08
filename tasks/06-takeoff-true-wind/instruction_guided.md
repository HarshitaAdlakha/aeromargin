You are a flight instructor checking a student's takeoff planning for a single-engine piston aircraft at 2,550 lb, short-field technique, flaps 10°.

**Takeoff distance table (from the aircraft's flight manual), feet**
Each cell is: ground roll / total distance to clear a 50 ft obstacle.

| Pressure altitude | 0 °C | 10 °C | 20 °C | 30 °C | 40 °C |
|---|---|---|---|---|---|
| Sea level | 860 / 1465 | 925 / 1575 | 995 / 1690 | 1070 / 1810 | 1150 / 1945 |
| 2000 ft | 1030 / 1740 | 1110 / 1875 | 1195 / 2015 | 1285 / 2165 | 1380 / 2330 |
| 4000 ft | 1235 / 2085 | 1335 / 2255 | 1440 / 2440 | 1550 / 2640 | 1670 / 2865 |

**Flight manual notes**
1. Decrease distances 10% for each 9 knots of headwind. For operation with tailwinds up to 10 knots, increase distances by 10% for each 2 knots. Apply these proportionally to the wind component (for example, 4.5 kt of headwind is a 5% decrease).
2. For operation on a dry, grass runway, increase distances by 15% of the "ground roll" figure (add the same amount to both the ground roll and the total distance).
3. Apply the wind correction first, then the surface correction.

**Today**
- Airfield elevation 1,450 ft; altimeter setting 29.62 inHg; outside air temperature 27 °C
- Runway 18, dry grass. The runway's magnetic heading is 178°.
- Wind, from the airfield's METAR: 260° at 14 kt, no gusts
- Local magnetic variation: 15° E
- Runway 18 take-off run available: 2,500 ft (published 2,700 ft; the first 200 ft are closed by NOTAM). The flying school's rule: total distance over 50 ft × 1.25 must not exceed the runway available.

**Method**
Pressure altitude = elevation + (29.92 − altimeter setting) × 1000 ft. Interpolate the table linearly in both pressure altitude and temperature. Use the wind as reported under that source's standard conventions, and resolve it onto the runway.

**Report**
1. Pressure altitude (ft)
2. Headwind component along the runway (kt; negative means tailwind)
3. Corrected ground roll (ft) and corrected total distance over 50 ft (ft)
4. Runway required under the school's rule (ft)
5. Whether the takeoff meets the school's rule (true/false)

Show your working. End your answer with a single JSON object in a ```json code block, with exactly these keys, plain numbers and a JSON boolean:

```json
{"pressure_altitude_ft": 0, "headwind_component_kt": 0, "ground_roll_ft": 0, "total_over_50ft_ft": 0, "required_runway_ft": 0, "meets_company_rule": true}
```
