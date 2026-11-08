"""Builds the Transcript Explorer (docs/app/): data.json from tasks + graded transcripts, plus a static index.html.
    python media/build_app.py"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from graders.grader import grade, load_task, task_ids  # noqa: E402

S = json.loads((ROOT / "results" / "summary.json").read_text(encoding="utf-8"))
ORDER = ["gpt-5.6-sol", "gpt-5.6-sol-low", "gpt-5.6-sol-none", "gpt-5.5", "gpt-5.5-low", "gpt-5.5-none", "gpt-5.4", "o3",
         "gpt-5.4-mini", "gemini-3.5-flash", "gemma-4-31b", "gpt-5.5@guided", "o3@guided", "gpt-5.4-mini@guided"]

tasks = []
for t in task_ids():
    task = load_task(t)
    tasks.append({"id": t, "title": task["title"], "area": task["area"], "why_hard": task["why_hard"], "failure_cost": task["failure_cost"],
                  "who": task["who"], "sources": task["sources"], "instruction": task["instruction"],
                  "reference": {k: task["reference"][k] for k in task["fields"]}, "fields": task["fields"],
                  "critical": [k for k, r in task["fields"].items() if r.get("critical")]})

runs = {}
cache = {}
for f in sorted((ROOT / "transcripts").glob("*/*/trial-*.json")):
    if f.parts[-3] in ("robustness", "oracle"):
        continue
    r = json.loads(f.read_text(encoding="utf-8"))
    if r.get("error"):
        continue
    key = (r["task"], r.get("variant", "realistic"))
    cache.setdefault(key, load_task(*key))
    g = grade(cache[key], r["response"])
    runs.setdefault(r["model"], {}).setdefault(r["task"], []).append({
        "trial": r["trial"], "passed": g["passed"], "score": g["score"], "answer": g.get("answer"),
        "wrong": {k: v["why"] for k, v in g["fields"].items() if not v["ok"]},
        "tokens": r["usage"].get("output_tokens"), "latency": r["latency_s"], "served": r["usage"].get("served_model"),
        "response": r["response"]})
for m in runs:
    for t in runs[m]:
        runs[m][t].sort(key=lambda x: x["trial"])

models = [m for m in ORDER if m in runs] + sorted(m for m in runs if m not in ORDER)
data = {"tasks": tasks, "models": [{"name": m, "pass_rate": S.get(m, {}).get("pass_rate"), "pass_hat_k": S.get(m, {}).get("pass_hat_k"),
                                    "effort": S.get(m, {}).get("settings", {}).get("reasoning_effort", "default")} for m in models], "runs": runs}
out = ROOT / "docs" / "app"
out.mkdir(parents=True, exist_ok=True)
(out / "data.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
print("wrote docs/app/data.json", round((out / "data.json").stat().st_size / 1e6, 2), "MB")
