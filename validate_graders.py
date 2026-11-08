"""Grader validation. No API calls, no network; runs in about a second.

For every task it checks that the grader:
  1. accepts the reference solution (score 1.0, pass)
  2. accepts the reference written differently: numbers as strings with commas and units,
     enums in upper case, booleans as strings, extra keys, and working shown before the JSON
  3. accepts every numeric field nudged to 80% of its tolerance (no false fails from rounding)
  4. rejects each critical field moved to 3x its tolerance (or flipped), one at a time
  5. rejects every trap answer in graders/traps.py (domain-specific wrong methods)
  6. rejects gaming: no JSON, the template echoed back, "pass|fail" hedges,
     a list of candidate answers, and a correct JSON followed by a different final JSON
Writes results/grader_validation.json and prints a summary. Exit code 1 if any check fails.

    python validate_graders.py
"""
import copy
import json
import sys
from pathlib import Path

from graders.grader import grade, load_task, task_ids
from graders.traps import traps_for

ROOT = Path(__file__).resolve().parent


def wrap(ans, prose="Working shown above.\n\n"):
    return f"{prose}```json\n{json.dumps(ans)}\n```"


def main():
    report, failures = {}, 0
    for tid in task_ids():
        task = load_task(tid)
        ref, fields = task["reference"], task["fields"]
        checks = []

        def expect(label, text, should_pass):
            nonlocal failures
            g = grade(task, text)
            ok = g["passed"] == should_pass and (not should_pass or g["score"] == 1.0)
            if not ok:
                failures += 1
            checks.append({"check": label, "expect": "pass" if should_pass else "fail",
                           "got": "pass" if g["passed"] else "fail", "score": g["score"], "ok": ok})

        expect("reference solution", wrap(ref), True)

        ref = {k: ref[k] for k in fields}   # only graded fields
        fmt = {}
        for k, v in ref.items():
            r = fields[k]
            if r["type"] == "number":
                fmt[k] = f"{v:,}"
            elif r["type"] == "enum":
                fmt[k] = str(v).upper()
            else:
                fmt[k] = str(v).lower()
        fmt["notes"] = "extra keys are ignored"
        expect("reference, reformatted (strings, commas, case, extra key)",
               "## Working\nStep 1 ... {not json}\n" + wrap(fmt), True)

        near = copy.deepcopy(ref)
        for k, r in fields.items():
            if r["type"] == "number":
                tol = max(r.get("tol_abs", 0), r.get("tol_rel", 0) * abs(ref[k]))
                near[k] = ref[k] + 0.8 * tol
        expect("every number nudged to 80% of tolerance", wrap(near), True)

        for k, r in fields.items():
            if not r.get("critical"):
                continue
            bad = copy.deepcopy(ref)
            if r["type"] == "number":
                tol = max(r.get("tol_abs", 0), r.get("tol_rel", 0) * abs(ref[k]))
                bad[k] = ref[k] + max(3 * tol, 1e-3 * max(1, abs(ref[k])), 1)
            elif r["type"] == "bool":
                bad[k] = not ref[k]
            else:
                bad[k] = "something_else"
            expect(f"critical field '{k}' wrong", wrap(bad), False)

        for label, ans in traps_for(tid).items():
            expect(f"trap: {label}", wrap(ans), False)

        tmpl = {k: (0 if r["type"] == "number" else ("pass|fail" if r["type"] == "enum" else True)) for k, r in fields.items()}
        hedge = {k: ("pass|fail" if r["type"] == "enum" else v) for (k, v), r in zip(ref.items(), fields.values())}
        listed = {k: ([v, "other"] if fields[k]["type"] == "enum" else [v, v * 1.5 if isinstance(v, float) else v]) for k, v in ref.items()}
        expect("gaming: no JSON at all", "The answer is " + ", ".join(f"{k} = {v}" for k, v in ref.items()), False)
        expect("gaming: template echoed back", wrap(tmpl), False)
        has_enum = any(r["type"] == "enum" for r in fields.values())
        if has_enum:
            expect("gaming: enum hedged as 'pass|fail'", wrap(hedge), False)
        expect("gaming: every field a list of candidates", wrap(listed), False)
        wrong_last = traps_for(tid)
        first_trap = next(iter(wrong_last.values()))
        expect("gaming: correct JSON, then a different final JSON", wrap(ref) + "\n\nOn reflection:\n" + wrap(first_trap), False)

        report[tid] = checks

    total = sum(len(v) for v in report.values())
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results" / "grader_validation.json").write_text(json.dumps(
        {"checks": total, "failures": failures, "tasks": report}, indent=2), encoding="utf-8")
    for tid, checks in report.items():
        bad = [c for c in checks if not c["ok"]]
        print(f"{tid:34s} {len(checks):3d} checks  {'OK' if not bad else 'FAIL'}")
        for c in bad:
            print(f"    !! {c['check']}: expected {c['expect']}, got {c['got']} (score {c['score']})")
    print(f"\n{total} checks, {failures} failures")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
