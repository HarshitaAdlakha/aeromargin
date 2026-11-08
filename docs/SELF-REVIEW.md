# Self-review against the judging rubric and the pre-submission checklist

Scored by us, honestly, before submitting. Evidence links point into this repository.

## Rubric (100 points)

| Criterion | Pts | Our evidence | Our honest gap |
|---|---|---|---|
| Real-world relevance | 15 | Each task is a check stress, fatigue, loads or operations people sign off; `task.json` → `who`, `failure_cost`; README *Who it's for*; market brief (79% unapproved AI use) | Synthetic numbers; no real program data (by design) |
| Task design | 20 | Every output and JSON key stated in the prompt; all data given; reference solution per task; standard methods with citations; ambiguity removed (stated fitting factor, Goodman, interpolation rules, stiffness ∝ area) | Two tasks (02, 04) turned out easy for most models: kept as "came close" controls |
| Grader reliability | 20 | Code graders only; `validate_graders.py` makes 133 checks (references, reformatting, 80%-of-tolerance, critical-field perturbation, 24 traps, 5 gaming patterns); oracle 10/10; transcript audit led to 3 tolerance fixes, all documented | Tolerances are our judgement; documented per field |
| Evidence of model limitations | 15 | 6 models, 3 trials per task, plus 2 reasoning-effort ablations, a guided-prompt ablation and a 12-variant robustness study; per-task failure notes with transcript links | The newest models at medium reasoning saturate the set (reported openly); Gemini 3.1 Pro quota-blocked; Flash/Gemma partial |
| Reproducibility | 15 | Stdlib-only Python; exact commands; model ids and served versions; settings; dates; cost and runtime; `summarize.py` re-grades from transcripts without API keys | Provider-side model updates can shift results |
| Human expertise and review | 10 | Traps chosen from practice; free bodies and section properties checked by hand; tolerance changes justified from transcripts; README states what AI drafted | AI assistant drafted code and prose (disclosed) |
| Insight / hot take | 5 | "Recall versus re-derive": reasoning setting matters more than the model; selection errors are cured by naming the method, knowledge errors (the lug exponent) are not | Based on 10 tasks |

## Pre-submission checklist (from the participant guide)

- [x] Every task has a reference solution that passes its grader (`validate_graders.py`, `run_eval.py --oracle`)
- [x] Deliberately wrong answers fail the grader (24 traps, critical-field perturbations, gaming patterns)
- [x] Everything the grader checks is stated in the task (keys, units, verdict labels, rounding-tolerant)
- [x] At least one frontier model tested, with multiple trials per task (GPT-5.6 Sol, GPT-5.5, GPT-5.4, o3; 3 trials)
- [x] We've read the failing transcripts and can explain why models fail (README → *Task by task*)
- [x] README explains how to run and reproduce, with versions, cost and runtime
- [x] ZIP opens, is under 50 MB and contains no videos (`package_zip.py` enforces it)
- [x] No API keys, passwords, confidential or private data in the ZIP (`package_zip.py` scans for key patterns; `.env` excluded)
- [x] Prior work disclosed (none in the eval; media tooling pattern reused)
- [ ] Video link opens without permission and plays with audio (check after uploading)
- [ ] Description is filled in (text in `docs/SUBMISSION TEXTS.md`)
- [x] Representative transcripts included for every model reported (`transcripts/`)
- [x] Scored our own project against the judging rubric (this file)
- [ ] Reviewed every task, reference answer and grading rule ourselves (Paras and Harshita: tick only after your own pass through `tasks/*/instruction.md`, `solution.py` and `task.json`)
