# Submission texts

Ready to paste into the HackerRank submission form, plus the video script and a social post. All numbers come from `results/summary.md` (runs on 8–9 Nov 2026).

---

## Form fields

**Project name:** AeroMargin

**Authors:** Paras Adlakha, Harshita Adlakha

**ZIP:** `dist/aeromargin.zip` (built by `python package_zip.py`; code, tasks, graders, results and transcripts; no videos, no keys)

**Video (≤ 5 min):** https://parasadlakha.github.io/aeromargin/video/AeroMargin-walkthrough.mp4

**Repository:** https://github.com/ParasAdlakha/aeromargin (mirror: https://github.com/HarshitaAdlakha/aeromargin)

**Project page:** https://parasadlakha.github.io/aeromargin/

**Short description:**

> AeroMargin is an aerospace engineering eval (airframe stress, fatigue, loads, flight performance, weight and balance) that tests whether a model picks the right method, and the right sign, before it calculates. Each of its 10 single-turn tasks contains one realistic condition that reverses a textbook default: a lug under oblique load, a short strut where Johnson governs, a tapered beam that is deeper at its free end, a METAR wind given in degrees true, a Z-section in unsymmetric bending. Every task has a reference solution and a deterministic code grader, validated by 133 checks (including 24 trap answers) before any model ran.
>
> We ran GPT-5.6 Sol, GPT-5.5, GPT-5.4, o3, GPT-5.4 mini and the open Gemma 4 31B with 3 trials per task. At medium reasoning, GPT-5.6 Sol and GPT-5.5 pass every trial. o3 passes 47% (pass^3 20%), GPT-5.4 mini 63%. The decisive variable is reasoning effort: with reasoning off, GPT-5.6 Sol drops to 60% and GPT-5.5 to 57%, and the failures are the textbook shortcuts themselves (a quadratic lug interaction that passes a failing fitting, the Resal relief applied to a beam that tapers the other way, a METAR wind read as magnetic). Headline: the gap is recall versus re-derive. The same model is right when it reasons and confidently wrong when it answers from memory.

**What existed before the hackathon:** Nothing in the eval. Tasks, data, reference solutions, graders, harness and analysis were built during the event. The slide/video tooling pattern (HTML → PNG → ffmpeg) was adapted from our earlier hackathon projects and is not part of the eval.

**AI use:** An AI coding assistant drafted the harness, grader, validation script and HTML pages, and helped search the literature. The tasks, traps and reference answers are our own and were checked by hand. Details are in the README (*AI use*).

---

## Video script (≈ 4½ min, 9 slides)

The narrated video is built by `python media/video.py` from `docs/slides/s1–s9.png`. The full narration is written to `media/build/narration.txt`.

| Slide | Time | Content |
|---|---|---|
| 1 | 0:00 | Title: what AeroMargin tests |
| 2 | 0:25 | Why it matters: 79% of A&D design engineers without approved AI tools use them anyway; a wrong margin looks like a right one |
| 3 | 0:55 | The ten tasks and their traps |
| 4 | 1:30 | Worked example: task 09, free body vs the textbook relief formula |
| 5 | 2:05 | Grading: code only, 133 validation checks, 24 traps, oracle, transcript audit |
| 6 | 2:40 | Results at medium reasoning |
| 7 | 3:15 | Reasoning effort: none / low / medium |
| 8 | 3:45 | Three failure transcripts |
| 9 | 4:15 | Hot take: recall versus re-derive |

---

## LinkedIn post (team voice)

> A stress engineer once told us: "The arithmetic is the easy part. The hard part is knowing which way the load goes."
>
> So for the micro1 Eval Hackathon we built **AeroMargin**: 10 aerospace hand calculations (lug fittings, struts, tapered beams, fatigue, gusts, takeoff planning), each with one condition that reverses a textbook default. Every task is graded by code against a reference solution.
>
> What we found:
> • At medium reasoning, GPT-5.6 Sol and GPT-5.5 got every trial right.
> • Turn reasoning off and the same models fall to 60% and 57%. The wrong answers were the textbook shortcuts themselves: a lug interaction that passes a failing fitting, a relief formula applied to a beam that tapers the other way, a METAR wind read as magnetic.
> • o3, last year's frontier reasoning model, passed 47%. It cited "Bruhn's elliptical interaction" on every lug trial. Bruhn's curve is the 1.6 power.
>
> Our takeaway: the gap is recall versus re-derive. If your team uses AI for engineering checks, the reasoning setting matters more than the leaderboard. Ask for the governing case and every load's direction before any number.
>
> Code, transcripts and all 10 tasks: https://github.com/ParasAdlakha/aeromargin
>
> #AerospaceEngineering #AIEvals #StressAnalysis #micro1
