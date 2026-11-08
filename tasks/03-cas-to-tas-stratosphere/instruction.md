A business jet is in level cruise. The crew wants a hand check of the flight-management system's air data.

**Conditions**
- Pressure altitude 41,000 ft (standard altimeter setting)
- Outside air temperature ISA + 10 °C
- Calibrated airspeed 250 kt (no instrument or position error)

**Constants to use**
ICAO Standard Atmosphere: 101,325 Pa and 288.15 K at sea level, lapse rate 0.0065 K/m to 11,000 m; g₀ = 9.80665 m/s²; R = 287.05287 J/(kg·K); γ = 1.4; 1 ft = 0.3048 m; 1 kt = 0.514444 m/s. Treat pressure altitude as geopotential altitude.

**Report**
1. Static pressure at the aircraft (Pa)
2. Outside air temperature (K)
3. Mach number
4. True airspeed (kt)
5. Density altitude (ft): the ICAO Standard Atmosphere altitude whose density equals the actual air density

Show your working. End with a single JSON object in a ```json code block, with exactly these keys and plain numbers:

```json
{"static_pressure_pa": 0, "oat_k": 0, "mach": 0, "tas_kt": 0, "density_altitude_ft": 0}
```
