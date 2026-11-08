# Submission texts

Ready to paste into the HackerRank submission form, plus the video script, a live demo script and social posts. All numbers come from `results/summary.md` (runs on 8–9 Nov 2026).

---

## Form fields

**Project name:** AeroMargin

**Authors:** Paras Adlakha, Harshita Adlakha

**ZIP:** `dist/aeromargin.zip` (built by `python package_zip.py`; code, tasks, graders, results and transcripts; no videos, no keys)

**Video (≤ 5 min):** https://parasadlakha.github.io/aeromargin/video/AeroMargin-walkthrough.mp4

**Repository:** https://github.com/ParasAdlakha/aeromargin (mirror: https://github.com/HarshitaAdlakha/aeromargin)

**Project page:** https://parasadlakha.github.io/aeromargin/

**Live app:** https://parasadlakha.github.io/aeromargin/app/#mode=live&task=09-inverted-taper-spar-web (run any task with your own key, or grade any answer; replay mode shows every saved transcript)

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

---

## Judging criteria, one line each

| Criterion | AeroMargin |
|---|---|
| Real-world relevance (15) | Ten checks that stress, fatigue, loads and operations people sign off; a wrong answer flips a certification verdict |
| Task design (20) | Every graded key stated, all data given, standard cited methods, a reference solution per task, one realistic trap each |
| Grader reliability (20) | Code-only graders; 133 validation checks incl. 24 traps and 5 gaming patterns; 17 unit tests; oracle 10/10; transcript audit |
| Evidence of model limitations (15) | 6 models × 3 trials plus effort, guided and robustness ablations; every failure explained with a transcript |
| Reproducibility (15) | Stdlib-only Python; 3 commands; `summarize.py` re-grades without keys; clean-room test of the ZIP |
| Human expertise and review (10) | Traps from practice; hand-derived references; tolerance changes justified from transcripts |
| Insight (5) | Recall versus re-derive: the reasoning setting matters more than the leaderboard |

---

## Live demo script (2 minutes)

Open https://parasadlakha.github.io/aeromargin/ and the explorer in a second tab.

1. **(15 s) Hook.** "A margin of safety of +0.71 and one of −0.08 look the same on a screen. Only one of them flies. AeroMargin asks whether a model picks the right method, and the right sign, before it calculates."
2. **(25 s) A task.** Explorer → task 09. Open *Prompt given to every model*. "The beam is deeper at its free end. Every textbook's relief formula assumes the opposite."
3. **(30 s) A failure.** Click `gpt-5.6-sol-none`. "Reasoning off: 4,200 lbf, pass, on three of three trials. It even writes that both flange components point up, then subtracts them." Click `gpt-5.6-sol`: "Reasoning on: 7,800 lbf, fail. Correct."
4. **(20 s) The grader.** In a terminal: `python validate_graders.py` → 133 checks, 0 failures. "Code only: references in, 24 trap answers out."
5. **(20 s) Results.** Project page table: medium reasoning 100% for the newest two; reasoning off 60% and 57%; o3 47%.
6. **(10 s) Close.** "The gap is recall versus re-derive. Ask for the governing case before any number."

---

## Event post (LinkedIn, team voice)

> We just submitted AeroMargin to the micro1 Eval Hackathon 🛩️
>
> The brief: find what AI can't do yet in a field you know, and measure it properly. Ours is aerospace hand calculations, the checks stress and performance engineers sign off every day.
>
> 10 tasks · reference solutions · code graders checked 133 ways before a single model ran · 6 models · 3 trials each · every transcript public.
>
> Explore every answer: https://parasadlakha.github.io/aeromargin/app/
>
> Thank you, micro1 and HackerRank, for a hackathon about rigour rather than demos.
>
> #AIEvals #AerospaceEngineering #micro1

## LinkedIn post (Paras, personal)

> In stress analysis we say the arithmetic is the easy part. The hard part is knowing which way the load goes.
>
> This week I tested that on language models. I wrote 10 aerospace hand calculations, each with one condition that reverses a textbook default: a beam that gets deeper toward its tip, a Z-section that bends sideways, a METAR wind given in degrees true.
>
> With full reasoning, the newest models got all of them right. With reasoning off, the same model wrote "both flange components point up", then subtracted them, because the formula it remembered subtracts.
>
> A requirement is a promise. A margin of safety is too. If you use AI for engineering checks, check the reasoning setting before you trust the number.
>
> Built with Harshita Adlakha for the micro1 Eval Hackathon. Code and transcripts: https://github.com/ParasAdlakha/aeromargin
>
> Views are my own.

## X post (under 280 characters)

> AeroMargin: 10 aerospace stress & performance checks, each reversing a textbook default. Newest models: 100% with reasoning on, ~60% with it off, and the misses are the textbook shortcuts themselves. Code-graded, every transcript public: github.com/ParasAdlakha/aeromargin
