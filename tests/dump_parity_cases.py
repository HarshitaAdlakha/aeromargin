"""Writes tests/parity_cases.json: every saved transcript plus every grader-validation case, with the Python
grader's verdict, so tests/grader_parity.mjs can check the browser grader against it."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from graders.grader import grade, load_task, task_ids  # noqa: E402
from graders.traps import traps_for  # noqa: E402

cases, tasks = [], {t: load_task(t) for t in task_ids()}
slim = lambda t: {"fields": t["fields"], "reference": {k: t["reference"][k] for k in t["fields"]}}


def add(cid, tid, text):
    g = grade(tasks[tid], text)
    cases.append({"id": cid, "task": slim(tasks[tid]), "text": text,
                  "py": {"passed": g["passed"], "score": g["score"], "fields": {k: v["ok"] for k, v in g["fields"].items()}}})


for f in sorted((ROOT / "transcripts").glob("*/*/trial-*.json")):
    if f.parts[-3] in ("robustness", "oracle"):
        continue
    r = json.loads(f.read_text(encoding="utf-8"))
    add(f"{r['model']}/{r['task']}/t{r['trial']}", r["task"], r.get("response", ""))
for t in task_ids():
    ref = slim(tasks[t])["reference"]
    add(f"{t}/reference", t, "```json\n" + json.dumps(ref) + "\n```")
    add(f"{t}/reformatted", t, "```json\n" + json.dumps({k: (f"{v:,}" if isinstance(v, (int, float)) and not isinstance(v, bool) else str(v).upper()) for k, v in ref.items()}) + "\n```")
    for label, ans in traps_for(t).items():
        add(f"{t}/trap/{label}", t, "```json\n" + json.dumps(ans) + "\n```")
    add(f"{t}/hedge", t, "```json\n" + json.dumps({k: "pass|fail" for k in ref}) + "\n```")
(Path(__file__).parent / "parity_cases.json").write_text(json.dumps(cases), encoding="utf-8")
print(len(cases), "cases written")
