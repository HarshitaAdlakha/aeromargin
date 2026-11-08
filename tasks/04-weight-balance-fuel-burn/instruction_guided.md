You are the dispatcher preparing the load sheet for a light business jet. All arms are in inches aft of the datum.

**Loading**

| Item | Weight (lb) | Arm (in) |
|---|---|---|
| Basic empty weight | 9,850 | 312.4 |
| Crew (2 × 190 lb) | 380 | 128.0 |
| Passengers, club seats (4 × 185 lb) | 740 | 335.0 |
| Passengers, aft bench (2 × 185 lb) | 370 | 372.0 |
| Aft baggage | 350 | 455.0 |

**Fuel**
- Ramp fuel: 660 US gal of Jet-A at 6.75 lb/US gal
- Taxi fuel burned before takeoff: 200 lb. Planned trip fuel burned from takeoff to landing: 2,600 lb.
- The fuel's centre of gravity moves as the tanks drain. Use this fuel moment table from the flight manual (moment ÷ 1000, in·lb, already at 6.75 lb/gal), interpolating linearly in moment between rows:

| US gal | 0 | 100 | 200 | 300 | 400 | 500 | 600 | 700 |
|---|---|---|---|---|---|---|---|---|
| Moment/1000 | 0.0 | 214.7 | 426.6 | 634.8 | 839.7 | 1041.2 | 1239.3 | 1436.4 |

**Limits**
- LEMAC = 288.0 in; MAC = 80.0 in; %MAC = (CG − LEMAC) / MAC × 100
- CG envelope at all weights: 15.0 % to 32.0 % MAC
- Maximum takeoff weight 16,600 lb; maximum landing weight 15,200 lb

**Report**
1. Takeoff weight (lb) and takeoff CG (%MAC)
2. Planned landing weight (lb) and landing CG (%MAC)
3. Whether the takeoff condition is within all the limits above (true/false)
4. Whether the planned landing condition is within all the limits above (true/false)

Show your working. End your answer with a single JSON object in a ```json code block, with exactly these keys, plain numbers and JSON booleans:

```json
{"takeoff_weight_lb": 0, "takeoff_cg_pct_mac": 0, "landing_weight_lb": 0, "landing_cg_pct_mac": 0, "takeoff_within_limits": true, "landing_within_limits": true}
```
