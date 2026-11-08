"""AeroMargin harness: run every task against one or more models, several trials each, grade, save.

    python run_eval.py --models gpt-5.5 gemini-3.1-pro --trials 3
    python run_eval.py --models gpt-5.4-mini --tasks 02 06 --trials 5
    python run_eval.py --oracle            # feeds each reference solution through the same pipeline
    python run_eval.py --models gpt-5.5 --variant guided   # ablation: method spelled out in the prompt

Standard library only. Keys come from the environment or a local .env (see .env.example).
Each trial is a fresh, single-turn request (no shared history between trials).
Outputs:
  transcripts/<model>/<task>/trial-<n>.json   prompt, full response, usage, latency, grade
  results/runs/<model>.jsonl                  one line per trial (appended)
Then run `python summarize.py` to build results/summary.md and results/summary.json.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from graders.grader import grade, load_task, task_ids

ROOT = Path(__file__).resolve().parent
CFG = json.loads((ROOT / "models.json").read_text(encoding="utf-8"))["models"]


def load_env():
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def post(url, body, headers, timeout=900):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"content-type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def call_model(cfg, prompt):
    """Return (text, usage dict, raw-settings dict)."""
    prov, model = cfg["provider"], cfg["model"]
    if prov in ("openai", "nvidia", "ollama"):
        url = {"openai": "https://api.openai.com/v1/chat/completions",
               "nvidia": "https://integrate.api.nvidia.com/v1/chat/completions",
               "ollama": "http://localhost:11434/v1/chat/completions"}[prov]
        key = {"openai": os.environ.get("OPENAI_API_KEY"), "nvidia": os.environ.get("NVIDIA_API_KEY"), "ollama": "ollama"}[prov]
        body = {"model": model, "messages": [{"role": "user", "content": prompt}]}
        if prov == "openai":
            body["max_completion_tokens"] = 32_000
            if cfg.get("reasoning_effort"):
                body["reasoning_effort"] = cfg["reasoning_effort"]
        else:
            body["max_tokens"] = 16_000
        j = post(url, body, {"authorization": f"Bearer {key}"})
        msg = j["choices"][0]["message"]
        text = msg.get("content") or ""
        u = j.get("usage") or {}
        det = u.get("completion_tokens_details") or {}
        usage = {"input_tokens": u.get("prompt_tokens", 0), "output_tokens": u.get("completion_tokens", 0),
                 "reasoning_tokens": det.get("reasoning_tokens", 0), "finish_reason": j["choices"][0].get("finish_reason"),
                 "served_model": j.get("model", model)}
        settings = {k: v for k, v in body.items() if k != "messages"}
        return text, usage, settings
    if prov == "gemini":
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}], "generationConfig": {"maxOutputTokens": 32_000}}
        j = post(url, body, {"x-goog-api-key": os.environ.get("GEMINI_API_KEY", "")})
        cand = (j.get("candidates") or [{}])[0]
        text = "".join(p.get("text", "") for p in (cand.get("content") or {}).get("parts", []) if not p.get("thought"))
        u = j.get("usageMetadata") or {}
        usage = {"input_tokens": u.get("promptTokenCount", 0),
                 "output_tokens": u.get("candidatesTokenCount", 0) + u.get("thoughtsTokenCount", 0),
                 "reasoning_tokens": u.get("thoughtsTokenCount", 0), "finish_reason": cand.get("finishReason"),
                 "served_model": j.get("modelVersion", model)}
        return text, usage, {"model": model, **body["generationConfig"]}
    raise ValueError(prov)


def run_trial(name, cfg, tid, trial, oracle=False, variant="realistic"):
    task = load_task(tid, variant)
    if variant == "guided":
        name = f"{name}@guided"
    prompt = task["instruction"]
    t0 = time.time()
    err = None
    if oracle:
        text = "Reference solution.\n```json\n" + json.dumps(task["reference"]) + "\n```"
        usage, settings = {"input_tokens": 0, "output_tokens": 0, "reasoning_tokens": 0}, {"oracle": True}
    else:
        text, usage, settings = "", {}, {}
        for attempt in range(5):
            try:
                text, usage, settings = call_model(cfg, prompt)
                err = None
                break
            except urllib.error.HTTPError as e:
                err = f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}"
            except Exception as e:  # network errors, timeouts
                err = f"{type(e).__name__}: {e}"
            time.sleep(20 * (attempt + 1))
    g = grade(task, text)
    price = cfg.get("price", [0, 0]) if cfg else [0, 0]
    cost = (usage.get("input_tokens", 0) * price[0] + usage.get("output_tokens", 0) * price[1]) / 1e6
    rec = {"model": name, "variant": variant, "task": tid, "trial": trial, "at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "latency_s": round(time.time() - t0, 1), "settings": settings, "usage": usage, "cost_usd": round(cost, 5),
           "error": err, "passed": g["passed"], "score": g["score"], "grade": g}
    out = ROOT / "transcripts" / name / tid
    out.mkdir(parents=True, exist_ok=True)
    (out / f"trial-{trial}.json").write_text(json.dumps({**rec, "prompt": prompt, "response": text}, indent=2, ensure_ascii=False), encoding="utf-8")
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=[])
    ap.add_argument("--tasks", nargs="*", default=[], help="task ids or 2-digit prefixes; default all")
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--oracle", action="store_true")
    ap.add_argument("--only-missing", action="store_true", help="run only trials with no transcript or an API error (e.g. after rate limits)")
    ap.add_argument("--variant", choices=["realistic", "guided"], default="realistic",
                    help="realistic = work-package prompt (default); guided = same task with the method spelled out")
    a = ap.parse_args()
    load_env()
    tids = [t for t in task_ids() if not a.tasks or any(t.startswith(x) for x in a.tasks)]
    names = ["oracle"] if a.oracle else a.models
    if not names:
        ap.error("give --models (see models.json) or --oracle")
    (ROOT / "results" / "runs").mkdir(parents=True, exist_ok=True)
    jobs = [(n, CFG.get(n), t, k) for n in names for t in tids for k in range(1, a.trials + 1)]
    if a.only_missing:
        def needed(n, t, k):
            f = ROOT / "transcripts" / (f"{n}@guided" if a.variant == "guided" else n) / t / f"trial-{k}.json"
            return not f.exists() or json.loads(f.read_text(encoding="utf-8")).get("error")
        jobs = [j for j in jobs if needed(j[0], j[2], j[3])]
    print(f"{len(jobs)} trials: {names} x {len(tids)} tasks x {a.trials}")
    with cf.ThreadPoolExecutor(a.workers) as ex:
        futs = [ex.submit(run_trial, n, c, t, k, a.oracle, a.variant) for n, c, t, k in jobs]
        for f in cf.as_completed(futs):
            r = f.result()
            with open(ROOT / "results" / "runs" / f"{r['model']}.jsonl", "a", encoding="utf-8") as fh:
                fh.write(json.dumps({k: v for k, v in r.items() if k != "grade"} | {"fields": {k: v["ok"] for k, v in r["grade"]["fields"].items()}}) + "\n")
            flag = "PASS" if r["passed"] else ("ERR " if r["error"] else "fail")
            print(f"{flag} {r['model']:20s} {r['task']:34s} t{r['trial']} score={r['score']:.2f} {r['latency_s']}s {r['error'] or ''}")


if __name__ == "__main__":
    main()
