# AeroMargin results

Same 10 tasks, same prompt, same grader for every model. A trial passes when every critical field is correct.

| Model (API id, settings) | Trials/task | Pass rate | Mean partial score | pass@k | pass^k | Trial-to-trial spread | Cost per full run | Mean latency |
|---|---|---|---|---|---|---|---|---|
| **gpt-5.6-sol** (`gpt-5.6-sol`, reasoning_effort=medium) | 3 | 100% | 1.00 | 100% | 100% | 100%–100% | $3.01 | 29 s |
| **gpt-5.6-sol-low** (`gpt-5.6-sol`, reasoning_effort=low) | 3 | 100% | 1.00 | 100% | 100% | 100%–100% | $1.85 | 18 s |
| **gpt-5.6-sol-none** (`gpt-5.6-sol`, reasoning_effort=none) | 3 | 60% | 0.74 | 80% | 40% | 50%–70% | $0.84 | 6 s |
| **gpt-5.5** (`gpt-5.5`, reasoning_effort=medium) | 3 | 100% | 1.00 | 100% | 100% | 100%–100% | $4.18 | 62 s |
| **gpt-5.5-low** (`gpt-5.5`, reasoning_effort=low) | 3 | 80% | 0.89 | 100% | 70% | 70%–90% | $1.73 | 23 s |
| **gpt-5.5-none** (`gpt-5.5`, reasoning_effort=none) | 3 | 57% | 0.72 | 70% | 30% | 50%–70% | $1.18 | 12 s |
| **gpt-5.4** (`gpt-5.4`, reasoning_effort=medium) | 3 | 97% | 1.00 | 100% | 90% | 90%–100% | $2.14 | 50 s |
| **o3** (`o3`, reasoning_effort=medium) | 3 | 47% | 0.66 | 70% | 20% | 30%–70% | $1.69 | 44 s |
| **gpt-5.4-mini** (`gpt-5.4-mini`, reasoning_effort=medium) | 3 | 63% | 0.79 | 80% | 40% | 60%–70% | $1.07 | 34 s |
| **gemini-3.5-flash** (`gemini-3.5-flash`, provider defaults) — **partial: 6/30 trials** (provider quota) | 3 | 100% | 1.00 | 100% | 33% | 100%–100% | $0.54 | 38 s |
| **gemma-4-31b** (`gemma-4-31b-it`, provider defaults) | 3 | 40% | 0.65 | 60% | 20% | 30%–50% | $0.00 | 288 s |
| **gpt-5.5@guided** (`gpt-5.5`, reasoning_effort=medium) | 3 | 100% | 1.00 | 100% | 100% | 100%–100% | $3.73 | 53 s |
| **o3@guided** (`o3`, reasoning_effort=medium) | 3 | 60% | 0.76 | 90% | 30% | 50%–80% | $2.05 | 64 s |
| **gpt-5.4-mini@guided** (`gpt-5.4-mini`, reasoning_effort=medium) | 3 | 70% | 0.85 | 80% | 50% | 60%–80% | $1.10 | 36 s |

## Passes per task (passes / trials)

| Task | gpt-5.6-sol | gpt-5.6-sol-low | gpt-5.6-sol-none | gpt-5.5 | gpt-5.5-low | gpt-5.5-none | gpt-5.4 | o3 | gpt-5.4-mini | gemini-3.5-flash | gemma-4-31b | gpt-5.5@guided | o3@guided | gpt-5.4-mini@guided |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01-oblique-lug-fitting | 3/3 | 3/3 | 1/3 | 3/3 | 1/3 | 0/3 | 3/3 | 0/3 | 0/3 | 3/3 | 0/3 | 3/3 | 0/3 | 0/3 |
| 02-short-strut-buckling | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 2/3 | 3/3 | 2/2 | 2/3 | 3/3 | 3/3 | 3/3 |
| 03-cas-to-tas-stratosphere | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 | 2/3 | 3/3 | 1/3 | 3/3 | 1/1 | 0/3 | 3/3 | 1/3 | 3/3 |
| 04-weight-balance-fuel-burn | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | – | 3/3 | 3/3 | 3/3 | 3/3 |
| 05-rainflow-fatigue-life | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 2/3 | 3/3 | 1/3 | 3/3 | – | 1/3 | 3/3 | 1/3 | 2/3 |
| 06-takeoff-true-wind | 3/3 | 3/3 | 1/3 | 3/3 | 1/3 | 0/3 | 3/3 | 3/3 | 2/3 | – | 0/3 | 3/3 | 3/3 | 3/3 |
| 07-gust-light-weight | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 2/3 | 3/3 | – | 0/3 | 3/3 | 2/3 | 2/3 |
| 08-eccentric-mixed-bolt-group | 3/3 | 3/3 | 2/3 | 3/3 | 1/3 | 2/3 | 3/3 | 0/3 | 0/3 | – | 2/3 | 3/3 | 2/3 | 0/3 |
| 09-inverted-taper-spar-web | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 | 0/3 | 3/3 | 0/3 | 1/3 | – | 3/3 | 3/3 | 2/3 | 3/3 |
| 10-z-section-unsymmetric-bending | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 2/3 | – | 1/3 | 3/3 | 1/3 | 2/3 |

## Most-missed fields per task (all models)

- **01-oblique-lug-fitting**: `ms_lug_oblique` ×22, `verdict` ×21
- **02-short-strut-buckling**: `critical_stress_psi` ×3, `critical_load_lbf` ×3, `ms` ×3, `verdict` ×2
- **03-cas-to-tas-stratosphere**: `mach` ×10, `tas_kt` ×10, `static_pressure_pa` ×2
- **04-weight-balance-fuel-burn**: `takeoff_cg_pct_mac` ×1
- **05-rainflow-fatigue-life**: `damage_per_flight` ×8, `life_flights` ×8, `cycles_per_flight` ×6, `largest_cycle_max_ksi` ×5
- **06-takeoff-true-wind**: `headwind_component_kt` ×11, `ground_roll_ft` ×11, `total_over_50ft_ft` ×11, `required_runway_ft` ×11
- **07-gust-light-weight**: `n_gust_min_weight` ×6, `design_n_min_weight` ×6, `n_gust_max_weight` ×5, `design_n_max_weight` ×4
- **08-eccentric-mixed-bolt-group**: `critical_bolt_load_lbf` ×15, `min_ms` ×15, `critical_bolt` ×14
- **09-inverted-taper-spar-web**: `web_shear_lbf` ×12, `web_tau_psi` ×12, `ms` ×12, `verdict` ×12
- **10-z-section-unsymmetric-bending**: `stress_A_psi` ×7, `stress_D_psi` ×7, `stress_B_psi` ×6, `stress_C_psi` ×6
