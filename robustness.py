"""Robustness study (GSM-Symbolic style) for the two sign-reasoning tasks.

Tasks 09 and 10 each hinge on getting a SIGN right from a free body. Here every combination of the
configuration flags is generated, with fresh numbers, so a model that recalls the textbook case
(rather than drawing the free body) is wrong on some combinations.

  09 tapered beam : taper (deeper toward the free end | shallower toward the free end)
                    x moment sense (upper flange in compression | in tension)
  10 Z-section    : top flange to the right | to the left  x  moment compresses the top | the bottom

Every variant has a reference computed in this file (same equations as tasks/*/solution.py).
    python robustness.py --models gpt-5.6-sol gpt-5.5 --trials 1
Writes transcripts/robustness/<model>/<variant>.json and results/robustness.json (+ prints a table).
"""
import argparse
import concurrent.futures as cf
import itertools
import json
from pathlib import Path

import run_eval
from graders.grader import check_field, extract_answer

ROOT = Path(__file__).resolve().parent

SPAR = """Stress check request: a cantilevered support beam (an I-section built from two flanges and a stiffened shear web), fixed at its inboard end, carrying loads near its outboard (free) end. {geom}

At the station being checked, the ultimate internal loads are:
- Shear: the loads outboard of the station add up to {V:,} lbf upward.
- Bending moment: {M:,} in·lb, putting the upper flange in {upper} and the lower flange in {lower}.

Distance between flange centroids at this station: {h} in. Web thickness: {t} in. Assume the flanges carry all the bending and the web carries a uniform shear stress over the depth. Web ultimate shear allowable Fsu = 30,000 psi (stiffened web; no buckling).

Report the shear force carried by the web at this station (lbf), the web shear stress (psi) and the margin of safety MS = Fsu / stress − 1.
End with a single JSON object in a ```json code block: {{"web_shear_lbf": 0, "web_tau_psi": 0, "ms": 0}}"""
DEEPER = "It is DEEPER at its free end than at its root: going outboard, the upper flange rises and the lower flange falls, each at a slope of {s} (tan α) relative to the beam's reference axis."
SHALLOWER = "It is SHALLOWER at its free end than at its root: going outboard, the upper flange falls and the lower flange rises, each at a slope of {s} (tan α) relative to the beam's reference axis."

ZSEC = """Stress check request: a cabin floor beam with a thin-walled Z cross-section (uniform thickness {t} in; use centre-line dimensions and the thin-wall approximation, dropping terms in t³).
- Web: vertical, {h} in between the flange centre lines
- Top flange: {b} in long, extending horizontally to the {top} from the top of the web
- Bottom flange: {b} in long, extending horizontally to the {bot} from the bottom of the web
Point A = free tip of the top flange; point B = top web–flange corner.

The beam is loaded vertically and has no lateral restraint. At the section checked, the bending moment is {M:,} in·lb about the horizontal centroidal axis, in the sense that compresses the {sense} of the section.

Report the bending stress at A and at B (psi, tension positive) and the largest magnitude of bending stress on the section.
End with a single JSON object in a ```json code block: {{"stress_A_psi": 0, "stress_B_psi": 0, "max_abs_stress_psi": 0}}"""


def spar_variants():
    nums = [dict(V=6000, M=180000, h=6.0, t=0.040, s=0.03), dict(V=4500, M=240000, h=8.0, t=0.032, s=0.025)]
    out = []
    for (deeper, upper_comp), n in itertools.product(itertools.product([True, False], [True, False]), nums):
        sign = +1 if (deeper == upper_comp) else -1   # flange components add to the web shear in these two cases
        v_web = n["V"] + sign * 2 * (n["M"] / n["h"]) * n["s"]
        tau = v_web / (n["h"] * n["t"])
        prompt = SPAR.format(geom=(DEEPER if deeper else SHALLOWER).format(s=n["s"]), V=n["V"], M=n["M"],
                             upper="compression" if upper_comp else "tension", lower="tension" if upper_comp else "compression",
                             h=n["h"], t=n["t"])
        vid = f"spar-{'deeper' if deeper else 'shallower'}-{'uppercomp' if upper_comp else 'uppertens'}-{n['V']}"
        textbook = sign == -1   # the familiar case: the textbook relief formula gives the right answer
        out.append(dict(id=vid, prompt=prompt, familiar=textbook,
                        ref={"web_shear_lbf": v_web, "web_tau_psi": tau, "ms": 30000 / tau - 1},
                        rules={"web_shear_lbf": {"type": "number", "tol_rel": 0.01}, "web_tau_psi": {"type": "number", "tol_rel": 0.01},
                               "ms": {"type": "number", "tol_abs": 0.01}}))
    return out


def z_variants():
    out = []
    for top_right, comp_top in itertools.product([True, False], [True, False]):
        t, h, b, mom = 0.08, 4.0, 1.25, 6000.0
        ix = t * h ** 3 / 12 + 2 * t * b * (h / 2) ** 2
        iy = 2 * (t * b ** 3 / 12 + t * b * (b / 2) ** 2)
        sx = 1 if top_right else -1
        ixy = 2 * (t * b) * (sx * b / 2) * (h / 2)
        mx = -mom if comp_top else mom
        den = ix * iy - ixy ** 2
        s = lambda x, y: mx * (iy * y - ixy * x) / den
        pa, pb = s(sx * b, h / 2), s(0, h / 2)
        pc, pd = s(0, -h / 2), s(-sx * b, -h / 2)
        prompt = ZSEC.format(t=t, h=h, b=b, top="RIGHT" if top_right else "LEFT", bot="LEFT" if top_right else "RIGHT",
                             M=int(mom), sense="top" if comp_top else "bottom")
        out.append(dict(id=f"zsec-top{'right' if top_right else 'left'}-{'comptop' if comp_top else 'compbottom'}", prompt=prompt,
                        familiar=(top_right and comp_top),
                        ref={"stress_A_psi": pa, "stress_B_psi": pb, "max_abs_stress_psi": max(abs(pa), abs(pb), abs(pc), abs(pd))},
                        rules={k: {"type": "number", "tol_rel": 0.01} for k in ("stress_A_psi", "stress_B_psi", "max_abs_stress_psi")}))
    return out


def run(model, v, trial):
    cfg = run_eval.CFG[model]
    text, usage, settings = run_eval.call_model(cfg, v["prompt"])
    ans = extract_answer(text) or {}
    fields = {k: check_field(r, v["ref"][k], ans.get(k)) for k, r in v["rules"].items()}
    ok = all(f[0] for f in fields.values())
    out = ROOT / "transcripts" / "robustness" / model
    out.mkdir(parents=True, exist_ok=True)
    rec = {"model": model, "variant": v["id"], "trial": trial, "familiar_case": v["familiar"], "passed": ok,
           "fields": {k: {"ok": a, "why": b} for k, (a, b) in fields.items()}, "reference": v["ref"],
           "usage": usage, "settings": settings, "prompt": v["prompt"], "response": text}
    (out / f"{v['id']}-t{trial}.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--trials", type=int, default=1)
    a = ap.parse_args()
    run_eval.load_env()
    variants = spar_variants() + z_variants()
    with cf.ThreadPoolExecutor(16) as ex:
        recs = [f.result() for f in cf.as_completed(
            [ex.submit(run, m, v, k) for m in a.models for v in variants for k in range(1, a.trials + 1)])]
    path = ROOT / "results" / "robustness.json"
    old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    keep = [r for r in old if r["model"] not in a.models]
    slim = [{k: r[k] for k in ("model", "variant", "trial", "familiar_case", "passed", "fields")} for r in recs]
    path.write_text(json.dumps(keep + slim, indent=2), encoding="utf-8")
    for m in a.models:
        rs = [r for r in recs if r["model"] == m]
        fam = [r for r in rs if r["familiar_case"]]
        unf = [r for r in rs if not r["familiar_case"]]
        print(f"{m:16s} familiar case {sum(r['passed'] for r in fam)}/{len(fam)}   reversed cases {sum(r['passed'] for r in unf)}/{len(unf)}")
        for r in sorted(rs, key=lambda r: r["variant"]):
            if not r["passed"]:
                print("   fail", r["variant"], {k: v["why"] for k, v in r["fields"].items() if not v["ok"]})


if __name__ == "__main__":
    main()
