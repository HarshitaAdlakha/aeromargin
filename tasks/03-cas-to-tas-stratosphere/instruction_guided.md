A business jet is in level cruise. The crew is checking the flight-management system's true airspeed and density altitude by hand.

**Conditions**
- Pressure altitude: 41,000 ft (standard altimeter setting)
- Outside air temperature: ISA + 10 °C at that pressure altitude
- Calibrated airspeed: 250 kt (assume no instrument or position error, so indicated = calibrated)

**Method and constants**
Use the ICAO Standard Atmosphere: sea-level pressure 101,325 Pa, sea-level temperature 288.15 K, lapse rate 0.0065 K/m up to 11,000 m geopotential, g₀ = 9.80665 m/s², R = 287.05287 J/(kg·K), γ = 1.4, 1 ft = 0.3048 m, 1 kt = 0.514444 m/s. Treat the pressure altitude as geopotential altitude. Air is compressible: do not use incompressible or rule-of-thumb conversions.

Density altitude is the altitude in the ICAO Standard Atmosphere at which the standard density equals the actual air density.

**Report**
1. Static pressure at the aircraft (Pa)
2. Outside air temperature (K)
3. Mach number
4. True airspeed (kt)
5. Density altitude (ft)

Show your working. End your answer with a single JSON object in a ```json code block, with exactly these keys and plain numbers:

```json
{"static_pressure_pa": 0, "oat_k": 0, "mach": 0, "tas_kt": 0, "density_altitude_ft": 0}
```
