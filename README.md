# AeroMargin

**Does the model pick the right method, and the right sign, before it calculates?** Ten aerospace hand-calculation tasks (airframe stress, fatigue, loads, flight performance, weight and balance), each with one condition that reverses a textbook default. Every task is graded by deterministic code against a reference solution.

Built by **Paras Adlakha** and **Harshita Adlakha** for the [micro1 Eval Hackathon](https://www.hackerrank.com/event/micro1-eval-hackathon) (30 Oct – 9 Nov 2026).

🎬 Video walkthrough: _link in the submission form_ · 🌐 [Project page](docs/index.html) · 📑 [Slides (PDF)](docs/slides/AeroMargin-slides.pdf) · [Research brief](docs/research-brief.html) · [Market brief](docs/market-brief.html)

---

## What it tests

Whether a language model, asked to do a stress check or a performance calculation the way a practitioner would receive it, **chooses the governing method and gets its direction right**: which interaction curve, which column regime, which layer of the atmosphere, which way the flange forces point, which reference north the wind is given in. The arithmetic is straightforward once the method is right. Each task is built so that the familiar textbook shortcut gives a confident answer that is wrong, and in most tasks it also flips the pass/fail verdict.

## Who it's for and why it matters

| Who | What they do with it | What a wrong answer costs |
|---|---|---|
| Airframe stress engineers (OEMs, Tier 1 suppliers, repair and STC shops) | Margins of safety for fittings, struts, beams, fastener groups | An unconservative margin in a certified load path: a failed static test, a redesign, an airworthiness directive |
| Fatigue and damage-tolerance engineers | Life estimates that set inspection thresholds | Inspections scheduled too late |
| Loads and certification engineers | Gust and maneuver envelopes | Structure under-designed at light weights |
| Pilots, instructors, dispatchers, load controllers | Air data, takeoff distance, load sheets | Runway excursions; landing outside the CG envelope |

Engineers already use chat models for this work: in a 2025 survey of 1,021 aerospace and defense engineering stakeholders, 79% of design engineers whose companies had **not** approved AI tools were using them anyway ([Molex](https://www.molex.com/en-us/industries-applications/defense-connectors/the-state-of-design-engineering-in-aerospace-and-defense)). A margin of safety that reads +0.71 when the truth is −0.08 looks exactly like a correct answer until an experienced checker redraws the free body. More in the [market brief](docs/market-brief.html).

---

## Headline results

<!-- RESULTS:START -->
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
| **gemma-4-31b** (`gemma-4-31b-it`, provider defaults) — **partial: 18/30 trials** (provider quota) | 3 | 33% | 0.64 | 50% | 17% | 17%–50% | $0.00 | 277 s |
| **gpt-5.5@guided** (`gpt-5.5`, reasoning_effort=medium) | 3 | 100% | 1.00 | 100% | 100% | 100%–100% | $3.73 | 53 s |
| **o3@guided** (`o3`, reasoning_effort=medium) | 3 | 60% | 0.76 | 90% | 30% | 50%–80% | $2.05 | 64 s |
| **gpt-5.4-mini@guided** (`gpt-5.4-mini`, reasoning_effort=medium) | 3 | 70% | 0.85 | 80% | 50% | 60%–80% | $1.10 | 36 s |

**Passes per task** (passes / trials)

| Task | gpt-5.6-sol | gpt-5.6-sol-low | gpt-5.6-sol-none | gpt-5.5 | gpt-5.5-low | gpt-5.5-none | gpt-5.4 | o3 | gpt-5.4-mini | gemini-3.5-flash | gemma-4-31b | gpt-5.5@guided | o3@guided | gpt-5.4-mini@guided |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01-oblique-lug-fitting | 3/3 | 3/3 | 1/3 | 3/3 | 1/3 | 0/3 | 3/3 | 0/3 | 0/3 | 3/3 | 0/3 | 3/3 | 0/3 | 0/3 |
| 02-short-strut-buckling | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 2/3 | 3/3 | 2/2 | 2/3 | 3/3 | 3/3 | 3/3 |
| 03-cas-to-tas-stratosphere | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 | 2/3 | 3/3 | 1/3 | 3/3 | 1/1 | 0/3 | 3/3 | 1/3 | 3/3 |
| 04-weight-balance-fuel-burn | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | – | 3/3 | 3/3 | 3/3 | 3/3 |
| 05-rainflow-fatigue-life | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 2/3 | 3/3 | 1/3 | 3/3 | – | 1/3 | 3/3 | 1/3 | 2/3 |
| 06-takeoff-true-wind | 3/3 | 3/3 | 1/3 | 3/3 | 1/3 | 0/3 | 3/3 | 3/3 | 2/3 | – | 0/3 | 3/3 | 3/3 | 3/3 |
| 07-gust-light-weight | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 2/3 | 3/3 | – | – | 3/3 | 2/3 | 2/3 |
| 08-eccentric-mixed-bolt-group | 3/3 | 3/3 | 2/3 | 3/3 | 1/3 | 2/3 | 3/3 | 0/3 | 0/3 | – | – | 3/3 | 2/3 | 0/3 |
| 09-inverted-taper-spar-web | 3/3 | 3/3 | 0/3 | 3/3 | 3/3 | 0/3 | 3/3 | 0/3 | 1/3 | – | – | 3/3 | 2/3 | 3/3 |
| 10-z-section-unsymmetric-bending | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 2/3 | – | – | 3/3 | 1/3 | 2/3 |

*Pass* = every critical field correct on that trial. *pass@k* / *pass^k* = share of tasks passed on at least one / on all of k trials. Cost per full run = 10 tasks × 3 trials at list prices. API errors (provider quota) are excluded and shown as partial coverage. Generated by `python summarize.py` from the saved transcripts.
<!-- RESULTS:END -->

**What this shows.** At their default (medium) reasoning effort, the two newest frontier models, gpt-5.6-sol and gpt-5.5, pass every trial of every task. Older and smaller models do not: o3, the frontier reasoning model of 2025, passes under half of its trials, and its pass^3 is 20%. The decisive variable is **reasoning effort**. With reasoning switched off, the setting behind fast "instant" chat modes, gpt-5.6-sol falls to 60% and gpt-5.5 to about half, and the failures are the textbook defaults this eval was built around. Details per task are [below](#task-by-task-what-failed-and-why).

---

## The tasks

Every task gives all the data needed, states every output the grader checks (with units and the JSON keys), and has a reference solution in `tasks/<id>/solution.py`. "Why it's hard" was written before any model was run; the model runs then confirmed it (or, for some models, did not).

| # | Task | Domain | Why it's hard (the trap) | If you fall for it |
|---|---|---|---|---|
| 01 | [Oblique-load lug fitting](tasks/01-oblique-lug-fitting/instruction.md) | Stress | Lugs under oblique load use Bruhn's interaction R<sub>a</sub><sup>1.6</sup> + R<sub>tr</sub><sup>1.6</sup> = 1, after the 1.5 factor of safety **and** the 1.15 fitting factor | Quadratic interaction gives MS +0.05 (**pass**); truth is MS −0.025 (**fail**) |
| 02 | [Short pinned strut](tasks/02-short-strut-buckling/instruction.md) | Stress | Euler stress (26,800 psi) is below yield, so Euler "looks valid", but L′/ρ = 60 is below the tangency ratio 74.7, so the Johnson parabola governs | Euler: MS +0.10 (pass); Johnson: MS −0.03 (fail) |
| 03 | [CAS → TAS at FL410, ISA+10](tasks/03-cas-to-tas-stratosphere/instruction.md) | Performance | Isothermal layer above 11 km, compressible pitot relation, speed of sound at the *actual* temperature, density altitude in the stratosphere | TAS off by 10–40 kt; density altitude off by ~260 ft |
| 04 | [Load sheet with fuel burn](tasks/04-weight-balance-fuel-burn/instruction.md) | W&B | The fuel's arm changes with quantity; burning forward fuel walks the CG aft | Constant fuel arm: landing at 31.05% MAC "in limits"; truth is 32.59%, past the 32.0% aft limit |
| 05 | [Rainflow fatigue life](tasks/05-rainflow-fatigue-life/instruction.md) | Fatigue | The damaging ground-air-ground cycle (−6 → 24 ksi) only appears when the repeating history is counted from its peak | Life overstated 12× (1.18 million vs 97,000 flights) |
| 06 | [Takeoff from METAR + chart + NOTAM](tasks/06-takeoff-true-wind/instruction.md) | Operations | METAR wind is in degrees **true**, runway headings magnetic (15° E variation); grass correction is 15% of the ground roll; a NOTAM cuts the take-off run available to 2,500 ft | Headwind 2.0 kt instead of 5.5; a missed NOTAM approves a takeoff that fails the rule |
| 07 | [Gust load factor vs weight](tasks/07-gust-light-weight/instruction.md) | Loads | Gust load factor *rises* as weight falls (4.08 at minimum weight, above the 3.8 maneuver limit); V<sub>A</sub> scales with √W | Treat max weight as critical; keep V<sub>A</sub> at 130 kt instead of 108.8 |
| 08 | [Eccentric bolt group, two sizes](tasks/08-eccentric-mixed-bolt-group/instruction.md) | Stress | Elastic method weighted by bolt area; the most-loaded bolt (L1) is **not** the critical one, the smaller R1/R3 are | Wrong critical bolt and margin |
| 09 | [Tapered beam deeper at its free end](tasks/09-inverted-taper-spar-web/instruction.md) | Stress | The Resal relief V − (M/h)(tan α₁ + tan α₂) holds only when depth grows with moment. Here the flange components *add* to the web shear | Web shear 4,200 lbf, MS +0.71 (**pass**); truth 7,800 lbf, MS −0.08 (**fail**). Unconservative by 86% |
| 10 | [Z-section floor beam](tasks/10-z-section-unsymmetric-bending/instruction.md) | Stress | A Z-section has I<sub>xy</sub> ≠ 0: the peak stress is twice My/I, and the tip of the "compressed" top flange is in **tension** | Peak stress halved; wrong sign at the flange tips |

Why each task matters to a practitioner, and the sources for every rule, are in `tasks/<id>/task.json` (`why_hard`, `failure_cost`, `sources`) and in the [research brief](docs/research-brief.html).

---

## Grading

All ten graders are **code** ([graders/grader.py](graders/grader.py)); there is no LLM judge.

- The model must end its answer with a JSON object whose keys are listed in the prompt. The grader reads the **last** ```json block (falling back to the last top-level `{…}` object), so it grades the final answer rather than the working. Any valid method passes.
- Each field has a rule in `task.json`: a number within an absolute or relative tolerance, a label from an accepted set, or a boolean. Numbers are normalised (thousands separators, unit suffixes, Unicode minus signs) before comparison.
- **Partial credit:** `score` = weighted share of correct fields. **Pass:** every field marked `critical` is correct. Critical fields are the ones a checker would sign off on: the governing margin, the verdict, the deciding quantity.
- Tolerances come from the precision of the inputs. For example, ±0.2% MAC is about the effect of rounding the CG to 0.1 in, and ±6% on fatigue life allows for rounding an equivalent stress to 3 significant figures (life goes as stress to the 6.7th power). Each tolerance sits well inside the distance to the nearest trap answer.

### How the grader was validated (no model in the loop)

```bash
python validate_graders.py      # 133 checks, about one second, no API calls
```

For every task, [validate_graders.py](validate_graders.py) checks that the grader:

1. **accepts the reference solution** (score 1.0)
2. accepts the same answer **reformatted**: numbers as strings with commas and units, labels in upper case, booleans as strings, extra keys, prose before the JSON
3. accepts every number **nudged to 80% of its tolerance** (no false fails from rounding)
4. **rejects each critical field** moved to 3× its tolerance or flipped, one at a time
5. **rejects every trap answer** in [graders/traps.py](graders/traps.py): 24 answers, each produced by a specific mistake a practitioner would recognise (no interaction curve, Euler instead of Johnson, wind taken as magnetic, missed NOTAM, textbook Resal sign, My/I on a Z-section…)
6. **rejects gaming**: no JSON at all, the template echoed back, `"pass|fail"` hedges, lists of candidate answers, and a correct JSON followed by a different final JSON

Result: **133 checks, 0 failures** ([results/grader_validation.json](results/grader_validation.json)). An oracle run then sends each reference solution through the same harness: `python run_eval.py --oracle` passes 10/10.

**Grader audit against transcripts.** We read every failing transcript to separate model mistakes from grader mistakes. Three model answers were failing on rounding rather than on substance, so we widened those tolerances and re-graded everything (`summarize.py` always re-grades from the saved transcripts with the current grader):

| Task | What we saw | Change |
|---|---|---|
| 04 | o3 rounded the CG to 0.1 in before converting: 32.7% MAC vs 32.59% | ±0.1 → ±0.2 % MAC (trap is 1.5% MAC away) |
| 06 | Models rounded the headwind to a whole knot (5 kt vs 5.47 kt), as pilots do | ±0.3 → ±0.6 kt (trap is 3.5 kt away) |
| 05 | gpt-5.5 (no reasoning) rounded Sa,eq and landed 3.6% off on life | ±3% → ±6% (traps are 127% and 1,100% away) |

After these changes no failure in the transcripts is a rounding or format artefact, except one o3 trial (task 07) that did the work correctly but gave no final JSON. That counts as a fail because the task requires the JSON.

---

## How to run

Requirements: **Python ≥ 3.10, standard library only** (tested on Python 3.14.6, Windows 11). No packages to install.

```bash
cp .env.example .env            # add OPENAI_API_KEY (and GEMINI_API_KEY for Gemini/Gemma)
python validate_graders.py      # 1. grader checks (no keys needed)
python run_eval.py --oracle     # 2. reference solutions through the full pipeline (no keys needed)
python run_eval.py --models gpt-5.6-sol gpt-5.5 --trials 3          # 3. models (names in models.json)
python run_eval.py --models gpt-5.6-sol-none --trials 3             # reasoning effort off
python run_eval.py --models gpt-5.5 --variant guided --trials 3     # ablation: method spelled out
python run_eval.py --models gemini-3.5-flash --trials 3 --workers 2 --only-missing   # resume after rate limits
python summarize.py             # 4. re-grade every transcript, write results/summary.md
python robustness.py --models gpt-5.6-sol --trials 1                # 5. sign-reversal variants of tasks 09 and 10
```

- Each trial is a fresh single-turn request with no shared history (clean state). Transcripts are written to `transcripts/<model>/<task>/trial-<n>.json` with the prompt, full response, token usage, latency, settings and grade.
- Model settings live in [models.json](models.json): API model id, reasoning effort, and list prices used for the cost column. OpenAI models use `max_completion_tokens = 32000`; Gemini models use `maxOutputTokens = 32000`. Temperature is left at each provider's default (reasoning models do not accept other values).
- **Cost and runtime.** One full run (10 tasks × 3 trials) costs about **$3–4** for gpt-5.6-sol or gpt-5.5 at medium effort, **$1–2** for gpt-5.4, o3 or gpt-5.4-mini, and **under $1** with reasoning off. Gemma ran on the free tier. With 16 parallel workers an OpenAI model takes **3–6 minutes**. Gemini Flash and Gemma take 30–60 minutes because of free-tier rate limits (use `--workers 2` and `--only-missing`). Exact per-model costs and latencies are in the results table.

---

## Results in detail

**Models tested** (all runs 8–9 Nov 2026, 3 trials per task, identical prompts and graders):

| Name in tables | API model id (served version) | Settings | Tier |
|---|---|---|---|
| gpt-5.6-sol / -low / -none | `gpt-5.6-sol` (served as `gpt-5.6-sol`) | reasoning_effort medium / low / none | Frontier (newest) |
| gpt-5.5 / -low / -none | `gpt-5.5` (`gpt-5.5-2026-04-23`) | reasoning_effort medium / low / none | Frontier |
| gpt-5.4 | `gpt-5.4` (`gpt-5.4-2026-03-05`) | medium | Frontier (previous) |
| o3 | `o3` (`o3-2025-04-16`) | medium | Frontier reasoning model, 2025 |
| gpt-5.4-mini | `gpt-5.4-mini` (`gpt-5.4-mini-2026-03-17`) | medium | Small |
| gemini-3.5-flash | `gemini-3.5-flash` (served as `gemini-3.6-flash`) | provider defaults | Small / fast. **Partial**: the free-tier daily quota ran out after 6 valid trials (tasks 01–03) |
| gemma-4-31b | `gemma-4-31b-it` (open weights, via the Gemini API) | provider defaults | Open model (free tier; see coverage in the table) |

Not tested, and why: **Gemini 3.1 Pro** returned HTTP 429 (quota exhausted) on every request with our key. **NVIDIA-hosted open models** (DeepSeek, Kimi, gpt-oss, Llama, Mistral) returned 404/410 or timed out on 8 Nov; the harness supports them (`provider: nvidia`). API errors are excluded from scores, and the affected trials were re-run.

<!-- TASKNOTES:START -->
### Task by task: what failed and why

Representative transcripts are linked; every trial is in `transcripts/<model>/<task>/`.

- **01 Oblique lug: the hardest task, and a knowledge gap.** 22 failing trials. **20 of them are the same answer**, MS ≈ +0.055 and "pass": a quadratic interaction R<sub>a</sub>² + R<sub>tr</sub>² = 1 instead of Bruhn's R<sub>a</sub><sup>1.6</sup> + R<sub>tr</sub><sup>1.6</sup> = 1. o3 writes on all three trials that "Bruhn D1 gives an elliptical interaction" ([transcript](transcripts/o3/01-oblique-lug-fitting/trial-1.json)). Naming the method in the prompt (guided variant) does **not** help o3 or GPT-5.4 mini: they do not know the exponent. GPT-5.6 Sol and GPT-5.5 get it right whenever they reason. The fitting factor was never the problem: every model applied it.
- **02 Short strut: models came close.** Almost every trial picks the Johnson parabola. The exceptions: Gemma chose Euler once (the trap), o3 once computed 12,180 psi from a wrong slenderness, and GPT-5.5 with reasoning off slipped once.
- **03 CAS → TAS: the method was right, the arithmetic slipped.** GPT-5.6 Sol with reasoning off used the isothermal layer and the compressible relation correctly, but miscalculated the impact pressure (10,636 Pa instead of 10,499 Pa), giving Mach 0.826–0.835 and TAS 484–490 kt instead of 0.840 and 493 kt on all three trials ([transcript](transcripts/gpt-5.6-sol-none/03-cas-to-tas-stratosphere/trial-1.json)). This is the one task where a calculator tool would likely fix the failure.
- **04 Load sheet: robust.** Only one GPT-5.4 mini trial failed (takeoff CG 29.19% vs 29.60%). No model used a constant fuel arm. The rounding fail we found here led to the ±0.2% MAC tolerance (see *Grader audit*).
- **05 Fatigue: rainflow is where o3 breaks.** Two of three o3 trials count 10.5–11 cycles without a closed ground-air-ground cycle (largest cycle 14 ksi instead of −6 → 24 ksi), which understates damage by over 20× ([transcript](transcripts/o3/05-rainflow-fatigue-life/trial-2.json)).
- **06 Takeoff: the METAR convention.** With reasoning off, GPT-5.5 (3/3 trials) and GPT-5.6 Sol (2/3) took the METAR wind as magnetic: 2.0 kt of headwind instead of 5.5 kt ([transcript](transcripts/gpt-5.5-none/06-takeoff-true-wind/trial-1.json)). No model missed the NOTAM, and every verdict on the school rule was right; the misses are in the distances.
- **07 Gust: robust.** Every model saw that light weight gives the higher gust load factor. Misses: GPT-5.4 scaled V<sub>A</sub> wrongly once (112.6 kt), and one o3 trial gave no final JSON.
- **08 Bolt group: most-loaded ≠ critical.** o3 (0/3) and GPT-5.4 mini (0/3) compute the area-weighted centroid correctly, then declare the large corner bolt L1 critical without checking the small R1/R3 bolts, whose margin is lowest ([transcript](transcripts/gpt-5.4-mini/08-eccentric-mixed-bolt-group/trial-1.json)).
- **09 Tapered beam: the sign.** o3 (0/3) either ignored the taper (6,000 lbf) or applied the textbook relief (4,200 lbf). GPT-5.6 Sol with reasoning off applied the relief on all three trials ([transcript](transcripts/gpt-5.6-sol-none/09-inverted-taper-spar-web/trial-1.json)). Guided prompts fix most of these: GPT-5.4 mini goes from 1/3 to 3/3 and o3 from 0/3 to 2/3.
- **10 Z-section: mostly right.** Misses flip every sign (o3) or use the wrong I<sub>x</sub> (GPT-5.4 mini, 0.9 instead of 0.675 in⁴), which halves the peak stress.
<!-- TASKNOTES:END -->

### Ablation 1: reasoning effort

The same model, the same prompts, only `reasoning_effort` changed (see the results table: gpt-5.6-sol and gpt-5.5 at medium, low and none). Turning reasoning off is the only change that makes the newest model fail. The failures are not random: with reasoning off, gpt-5.6-sol answered task 09 with the textbook Resal relief on **all three** trials (4,200 lbf, MS +0.71, "pass"), and task 01 with a quadratic interaction on two of three. With reasoning on, it drew the free body every time.

<!-- GUIDED:START -->
### Ablation 2: method spelled out ("guided" prompts)

`instruction_guided.md` is the first draft of each task, which names the method (for example "use the oblique-load interaction curve of Bruhn D1.8", "use the Johnson parabola below the tangency slenderness", "for this geometry decide whether the flange components relieve or add"). We kept it as an ablation. GPT-5.5 scores 100% either way. o3 goes from 47% to 60% and GPT-5.4 mini from 63% to 70%. The gains are on tasks 08 and 09 (method *selection*: once told, they apply it). On task 01 they stay at 0/3: told to use Bruhn's curve, they still use the wrong one. **Selection errors are cured by naming the method; knowledge errors are not.**
<!-- GUIDED:END -->

### Ablation 3: sign-reversal robustness (GSM-Symbolic style)

[robustness.py](robustness.py) generates every combination of the configuration flags for tasks 09 (taper direction × moment sense, two sets of numbers) and 10 (flange orientation × moment sense), each with a computed reference. This tests whether a model that passes task 09 is reasoning from the free body or got lucky with one configuration. gpt-5.6-sol and gpt-5.5 at medium effort passed all 12 variants (5/5 familiar, 7/7 reversed; [results/robustness.json](results/robustness.json)). The passes at medium effort are real.

---

## Main failure mode and hot take

**The failure is not arithmetic. It is the reflex of using the textbook default.** Across models, the wrong answers are the specific shortcuts in our trap list, reproduced almost exactly: Ra² + Rtr² = 1 instead of the 1.6 exponent (MS +0.055, in 20 of the 22 failing lug trials), V − (M/h)Σtan α regardless of which way the beam tapers (4,200 lbf), the METAR wind used as magnetic (2 kt), the most-loaded bolt taken as critical. One o3 transcript states that "Bruhn D1 gives an elliptical interaction", which it does not.

**Hot take: in this domain, the gap between a passing model and a failing one is whether it *re-derives* or *recalls*.** The same model (gpt-5.6-sol) is 100% correct when allowed to reason, and with reasoning off it fails at least two of three trials on four of the ten tasks, choosing the familiar formula with total confidence. For engineering teams that means two things. A model's score on textbook-style questions says little about its use as a checker's assistant: what matters is the reasoning setting it is run at. And the cheapest guard is procedural: require the model to state the governing case and the direction of every load before any number, which is exactly what a senior checker asks of a junior engineer. Closing the gap for good needs training data where the textbook case is reversed, the kind of variants `robustness.py` generates.

---

## Reproducibility checklist

- Exact commands, dependencies (none) and Python version above. Data: everything is in the prompts; no external files.
- Model ids, served versions, reasoning settings, token limits and dates are recorded in every transcript (`settings`, `usage.served_model`, `at`).
- `summarize.py` re-grades from the transcripts, so anyone can verify our table from the submitted files without an API key.
- Expected results: the table above. Model outputs vary between runs; with 3 trials, expect about ±1 task per model.

## Provenance and licences

- **Everything was built during the hackathon** (8–9 Nov 2026): all ten tasks, data, reference solutions, graders, traps, harness and analysis. No task is adapted from an existing benchmark.
- **Borrowed ideas, credited:** the task / reference-solution / tests structure and oracle runs (Terminal-Bench / Harbor), pass^k (τ-bench), graded variants (GSM-Symbolic). The engineering methods are standard and cited per task (Bruhn; Megson; Niu; ASTM E1049; ICAO Doc 7488; 14 CFR Parts 23, 25 and 121; FAA handbooks).
- **Data:** all numbers are synthetic, written for this eval. Tables are invented but realistic and copy no manufacturer's flight manual. No confidential, employer or personal data.
- **Code licence:** MIT ([LICENSE](LICENSE)). Model outputs in `transcripts/` were generated through the providers' APIs under their terms of service.

## AI use

We used an AI coding assistant to draft the harness, the grader, the validation script, the HTML pages and parts of this README, and to search the literature. The tasks are ours. We chose each trap because it is a mistake we know practitioners make, and we wrote or checked every reference solution by hand: free-body diagrams for tasks 01, 08 and 09, the Z-section properties for task 10 (I<sub>x</sub> = 0.675, I<sub>y</sub> = 0.0667, I<sub>xy</sub> = 0.15 in⁴), and the atmosphere, compressible-flow and rainflow numbers for tasks 03 and 05, against independent calculations. We read every failing transcript before writing the analysis, and that reading is what led to the three tolerance changes listed under *Grader audit*. Where a draft task turned out ambiguous or too easy we rewrote it and say so above (the "guided" prompts are the first drafts).

## Limitations

- Ten tasks is a small sample. One trial more or less moves a model by 3 percentage points, so treat differences under ~10 points as noise.
- Only one provider's frontier models could be run at medium/high effort (Gemini 3.1 Pro was quota-blocked), so "frontier" here means OpenAI's frontier plus Gemini Flash and Gemma.
- Single-turn tasks: no tools, no code execution. Several failures (e.g. the arithmetic slip in task 03 with reasoning off) would likely disappear with a calculator tool; the method errors (01, 06, 09) would not.
- At medium effort the newest models saturate this set. The next version needs more reversed-default tasks per area, which `robustness.py` shows how to generate.

## Repository layout

```
aeromargin/
├── README.md               this file
├── tasks/<id>/             instruction.md (prompt), instruction_guided.md (ablation), solution.py (reference), task.json (grading rules, why hard, sources)
├── graders/grader.py       code-based grader (parse last JSON, tolerances, partial credit, critical fields)
├── graders/traps.py        24 deliberately wrong answers, each from a known mistake
├── validate_graders.py     133 grader checks, no API calls
├── run_eval.py             harness (stdlib only): models × tasks × trials, transcripts, --oracle, --variant, --only-missing
├── summarize.py            re-grades all transcripts, writes results/summary.md and summary.json
├── robustness.py           sign-reversal variants of tasks 09 and 10
├── models.json             model ids, reasoning settings, list prices
├── results/                summary.md, summary.json, grader_validation.json, robustness.json, run logs
├── transcripts/            every trial: prompt, full response, usage, settings, grade
├── docs/                   project page, research and market briefs, slides
├── requirements.txt        (none: standard library only)
└── .env.example            key names only
```

## Authors

**Paras Adlakha** and **Harshita Adlakha**. Questions and corrections are welcome as GitHub issues.
