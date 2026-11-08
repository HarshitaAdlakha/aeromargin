"""Re-grade all transcripts and aggregate them into results/summary.json and results/summary.md.

Metrics per model (k = trials per task):
  pass rate   share of all trials that passed (every critical field correct)
  mean score  mean partial-credit score over all trials
  pass@k      share of tasks passed at least once in k trials
  pass^k      share of tasks passed in every one of k trials (consistency)
  spread      min-max of per-trial-index pass rates (trial 1 vs 2 vs 3 ...)
Cost is recomputed from recorded token usage and the list prices in models.json.

    python summarize.py
"""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CFG = json.loads((ROOT / "models.json").read_text(encoding="utf-8"))["models"]
ORDER = ["gpt-5.6-sol", "gpt-5.6-sol-low", "gpt-5.6-sol-none", "gpt-5.5", "gpt-5.5-low", "gpt-5.5-none", "gpt-5.4", "o3",
         "gpt-5.4-mini", "gemini-3.5-flash", "gemma-4-31b",
         "gpt-5.5@guided", "o3@guided", "gpt-5.4-mini@guided"]


def load():
    """Re-grade every saved transcript with the CURRENT grader, so results always match graders/ and tasks/."""
    from graders.grader import grade, load_task
    cache, rows = {}, []
    for f in sorted((ROOT / "transcripts").glob("*/*/trial-*.json")):
        if f.parts[-3] == "robustness":
            continue
        t = json.loads(f.read_text(encoding="utf-8"))
        key = (t["task"], t.get("variant", "realistic"))
        if key not in cache:
            cache[key] = load_task(*key)
        g = grade(cache[key], t.get("response", ""))
        rows.append({**{k: t[k] for k in ("model", "task", "trial", "at", "latency_s", "settings", "usage", "error")},
                     "passed": g["passed"], "score": g["score"], "fields": {k: v["ok"] for k, v in g["fields"].items()}})
    return rows


def main():
    all_rows = [r for r in load() if r["model"] != "oracle"]
    api_errors = collections.Counter(r["model"] for r in all_rows if r.get("error"))
    rows = [r for r in all_rows if not r.get("error")]  # API failures (rate limits) are not model answers
    by_model = collections.defaultdict(list)
    for r in rows:
        by_model[r["model"]].append(r)
    tasks = sorted({r["task"] for r in rows})
    summary = {}
    for m, rs in by_model.items():
        base = m.split("@")[0]
        price = CFG.get(base, {}).get("price", [0, 0])
        k = max(r["trial"] for r in rs)
        per_task = collections.defaultdict(list)
        for r in sorted(rs, key=lambda r: r["trial"]):
            per_task[r["task"]].append(r)
        per_trial = collections.defaultdict(list)
        for r in rs:
            per_trial[r["trial"]].append(r["passed"])
        cost = sum((r["usage"].get("input_tokens", 0) * price[0] + r["usage"].get("output_tokens", 0) * price[1]) / 1e6 for r in rs)
        n_runs = len(rs) / max(1, len(per_task) * k)
        trial_rates = [sum(v) / len(v) for v in per_trial.values()]
        summary[m] = {
            "model_id": CFG.get(base, {}).get("model", base),
            "served_model": sorted({r["usage"].get("served_model", "") for r in rs if r["usage"].get("served_model")}),
            "settings": rs[0].get("settings", {}),
            "tier": CFG.get(base, {}).get("tier", ""),
            "trials_per_task": k,
            "n_trials": len(rs),
            "api_errors_excluded": api_errors.get(m, 0),
            "pass_rate": sum(r["passed"] for r in rs) / len(rs),
            "mean_score": sum(r["score"] for r in rs) / len(rs),
            "pass_at_k": sum(any(r["passed"] for r in v) for v in per_task.values()) / len(per_task),
            "pass_hat_k": sum(all(r["passed"] for r in v) and len(v) == k for v in per_task.values()) / len(per_task),
            "trial_pass_rate_min": min(trial_rates), "trial_pass_rate_max": max(trial_rates),
            "cost_usd_full_run": cost / max(n_runs, 1e-9) if n_runs else cost,
            "mean_latency_s": sum(r["latency_s"] for r in rs) / len(rs),
            "mean_output_tokens": sum(r["usage"].get("output_tokens", 0) for r in rs) / len(rs),
            "dates": sorted({r["at"][:10] for r in rs}),
            "tasks": {t: {"passes": sum(r["passed"] for r in v), "trials": len(v),
                          "mean_score": round(sum(r["score"] for r in v) / len(v), 3),
                          "failed_fields": dict(collections.Counter(f for r in v for f, ok in r["fields"].items() if not ok))}
                      for t, v in sorted(per_task.items())},
        }
    (ROOT / "results" / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    models = [m for m in ORDER if m in summary] + sorted(m for m in summary if m not in ORDER)
    pct = lambda x: f"{100 * x:.0f}%"
    L = ["# AeroMargin results", "",
         "Same 10 tasks, same prompt, same grader for every model. A trial passes when every critical field is correct.", "",
         "| Model (API id, settings) | Trials/task | Pass rate | Mean partial score | pass@k | pass^k | Trial-to-trial spread | Cost per full run | Mean latency |",
         "|---|---|---|---|---|---|---|---|---|"]
    for m in models:
        s = summary[m]
        st = s["settings"]
        setting = ", ".join(f"{k}={v}" for k, v in st.items() if k in ("reasoning_effort",)) or "provider defaults"
        full = len(tasks) * s["trials_per_task"]
        note = f" — **partial: {s['n_trials']}/{full} trials** (provider quota)" if s["n_trials"] < full else ""
        L.append(f"| **{m}** (`{s['model_id']}`, {setting}){note} | {s['trials_per_task']} | {pct(s['pass_rate'])} | {s['mean_score']:.2f} | "
                 f"{pct(s['pass_at_k'])} | {pct(s['pass_hat_k'])} | {pct(s['trial_pass_rate_min'])}–{pct(s['trial_pass_rate_max'])} | "
                 f"${s['cost_usd_full_run']:.2f} | {s['mean_latency_s']:.0f} s |")
    L += ["", "## Passes per task (passes / trials)", "", "| Task | " + " | ".join(models) + " |", "|---|" + "---|" * len(models)]
    for t in tasks:
        cells = []
        for m in models:
            v = summary[m]["tasks"].get(t)
            cells.append(f"{v['passes']}/{v['trials']}" if v else "–")
        L.append(f"| {t} | " + " | ".join(cells) + " |")
    L += ["", "## Most-missed fields per task (all models)", ""]
    for t in tasks:
        c = collections.Counter()
        for m in models:
            c.update(summary[m]["tasks"].get(t, {}).get("failed_fields", {}))
        L.append(f"- **{t}**: " + (", ".join(f"`{f}` ×{n}" for f, n in c.most_common(4)) or "none"))
    (ROOT / "results" / "summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    readme = ROOT / "README.md"
    if readme.exists():
        import re
        body = "\n".join(L[2:L.index("## Most-missed fields per task (all models)")]).replace("## Passes per task", "**Passes per task**").strip()
        body += ("\n\n*Pass* = every critical field correct on that trial. *pass@k* / *pass^k* = share of tasks passed on at least one / on all "
                 "of k trials. Cost per full run = 10 tasks × 3 trials at list prices. API errors (provider quota) are excluded and shown as partial "
                 "coverage. Generated by `python summarize.py` from the saved transcripts.")
        txt = readme.read_text(encoding="utf-8")
        txt = re.sub(r"<!-- RESULTS:START -->.*?<!-- RESULTS:END -->",
                     lambda _: "<!-- RESULTS:START -->\n" + body + "\n<!-- RESULTS:END -->", txt, flags=re.S)
        readme.write_text(txt, encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
