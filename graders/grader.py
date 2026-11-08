"""Code-based grader for AeroMargin.

A model's answer is graded from the LAST ```json block in its response (falling back to the last
top-level {...} object). Each field is compared with the reference solution's value using the
field's rule in tasks/<id>/task.json:

  number : |got - want| <= tol_abs, or |got - want| <= tol_rel * |want|
  enum   : normalised string must equal one accepted value (no lists, no "a|b" echoes)
  bool   : JSON boolean, or the strings "true"/"false"

score   = weighted fraction of fields correct (partial credit)
passed  = every field marked "critical" is correct
"""
from __future__ import annotations

import importlib.util
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "tasks"


def load_task(task_id: str, variant: str = "realistic") -> dict:
    d = TASKS / task_id
    meta = json.loads((d / "task.json").read_text(encoding="utf-8"))
    spec = importlib.util.spec_from_file_location(f"sol_{task_id.replace('-', '_')}", d / "solution.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ref = {k: v for k, v in mod.solve().items() if not k.startswith("_")}
    meta["reference"] = ref
    fname = "instruction_guided.md" if variant == "guided" else "instruction.md"
    meta["instruction"] = (d / fname).read_text(encoding="utf-8")
    meta["variant"] = variant
    return meta


def task_ids() -> list[str]:
    return sorted(p.name for p in TASKS.iterdir() if (p / "task.json").exists())


# ---------------------------------------------------------------- parsing
_FENCE = re.compile(r"```(?:json|JSON)?\s*(\{.*?\})\s*```", re.S)


def _last_object(text: str):
    """Last balanced top-level {...} in text that parses as JSON."""
    found = None
    depth, start = 0, None
    in_str, esc = False, False
    for i, ch in enumerate(text):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"' and depth > 0:
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}" and depth > 0:
            depth -= 1
            if depth == 0:
                try:
                    found = json.loads(text[start:i + 1])
                except json.JSONDecodeError:
                    pass
    return found


def extract_answer(text: str):
    if not text:
        return None
    blocks = _FENCE.findall(text)
    for b in reversed(blocks):
        try:
            obj = json.loads(b)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            obj = _last_object(b)
            if isinstance(obj, dict):
                return obj
    obj = _last_object(text)
    return obj if isinstance(obj, dict) else None


# ---------------------------------------------------------------- normalising
def to_number(v):
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v) if math.isfinite(v) else None
    if isinstance(v, str):
        s = v.strip().replace(",", "").replace("−", "-")
        s = re.sub(r"(?i)\s*(lbf|lb|psi|ksi|kt|kts|keas|ft|in|pa|k|%|flights)$", "", s)
        if re.fullmatch(r"[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?", s):
            return float(s)
    return None


def to_enum(v):
    if not isinstance(v, str):
        return None
    s = v.strip().strip(".").strip().lower().replace("-", "_").replace(" ", "_")
    if "|" in s or "/" in s or "," in s:
        return None  # an echoed template or a hedge like "pass/fail" is not an answer
    return s


def to_bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, str) and v.strip().lower() in ("true", "false"):
        return v.strip().lower() == "true"
    return None


def check_field(rule: dict, want, got) -> tuple[bool, str]:
    kind = rule["type"]
    if kind == "number":
        g = to_number(got)
        if g is None:
            return False, f"not a number: {got!r}"
        w = float(want)
        tol = max(rule.get("tol_abs", 0.0), rule.get("tol_rel", 0.0) * abs(w))
        ok = abs(g - w) <= tol + 1e-12
        return ok, f"got {g:g}, want {w:g} ± {tol:g}"
    if kind == "enum":
        g = to_enum(got)
        accepted = [a.lower() for a in rule.get("accept", [want])]
        return g in accepted, f"got {got!r}, want one of {accepted}"
    if kind == "bool":
        g = to_bool(got)
        return g is not None and g == bool(want), f"got {got!r}, want {want}"
    raise ValueError(kind)


def grade(task: dict, response_text: str) -> dict:
    ans = extract_answer(response_text)
    fields = task["fields"]
    if ans is None:
        return {"parsed": False, "score": 0.0, "passed": False,
                "fields": {k: {"ok": False, "why": "no JSON answer found"} for k in fields}}
    out, num, den, passed = {}, 0.0, 0.0, True
    for name, rule in fields.items():
        want = task["reference"][name]
        if name not in ans:
            ok, why = False, "missing"
        else:
            ok, why = check_field(rule, want, ans[name])
        w = rule.get("weight", 1.0)
        den += w
        num += w if ok else 0.0
        if rule.get("critical") and not ok:
            passed = False
        out[name] = {"ok": ok, "why": why, "critical": bool(rule.get("critical"))}
    return {"parsed": True, "score": round(num / den, 4), "passed": passed, "fields": out, "answer": ans}


if __name__ == "__main__":
    for t in task_ids():
        print(t, load_task(t)["reference"])
