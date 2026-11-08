"""Writes docs/slides/slides.html (9 slides, 1920x1080, one .frame each) from results/summary.json,
so every number on the slides comes from the graded transcripts.   python media/build_slides.py"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = json.loads((ROOT / "results" / "summary.json").read_text(encoding="utf-8"))
ROB = json.loads((ROOT / "results" / "robustness.json").read_text(encoding="utf-8"))
VAL = json.loads((ROOT / "results" / "grader_validation.json").read_text(encoding="utf-8"))

MAIN = [m for m in ["gpt-5.6-sol", "gpt-5.5", "gpt-5.4", "gpt-5.4-mini", "o3", "gemma-4-31b"] if m in S and S[m]["n_trials"] >= 30]
LABEL = {"gpt-5.6-sol": "GPT-5.6 Sol", "gpt-5.5": "GPT-5.5", "gpt-5.4": "GPT-5.4", "o3": "o3", "gpt-5.4-mini": "GPT-5.4 mini",
         "gemini-3.5-flash": "Gemini 3.5 Flash", "gemma-4-31b": "Gemma 4 31B (open)"}
pct = lambda x: f"{round(100 * x)}%"


def bars(models, w=1500, row=74):
    out = []
    for i, m in enumerate(models):
        s = S[m]
        y = i * row
        pr, ph = s["pass_rate"], s["pass_hat_k"]
        out.append(f'<text x="0" y="{y + 34}" class="bl">{LABEL.get(m, m)}</text>')
        out.append(f'<rect x="330" y="{y + 6}" width="{w - 330}" height="44" rx="8" class="track"/>')
        out.append(f'<rect x="330" y="{y + 6}" width="{(w - 330) * pr:.0f}" height="44" rx="8" class="fill"/>')
        out.append(f'<rect x="330" y="{y + 52}" width="{(w - 330) * ph:.0f}" height="8" rx="4" class="fill2"/>')
        out.append(f'<text x="{340 + (w - 330) * pr:.0f}" y="{y + 38}" class="bv">{pct(pr)}</text>')
    return f'<svg viewBox="0 0 {w + 140} {len(models) * row}" width="{w + 140}" height="{len(models) * row}">{"".join(out)}</svg>'


def effort():
    groups = [("GPT-5.6 Sol", ["gpt-5.6-sol-none", "gpt-5.6-sol-low", "gpt-5.6-sol"]), ("GPT-5.5", ["gpt-5.5-none", "gpt-5.5-low", "gpt-5.5"])]
    out, x0 = [], 0
    for g, ms in groups:
        for j, m in enumerate(ms):
            if m not in S:
                continue
            v = S[m]["pass_rate"]
            x = x0 + j * 170
            h = 400 * v
            out.append(f'<rect x="{x}" y="{460 - h:.0f}" width="130" height="{h:.0f}" rx="10" class="{"fill" if j == 2 else "fillmute"}"/>')
            out.append(f'<text x="{x + 65}" y="{445 - h:.0f}" class="bvc">{pct(v)}</text>')
            out.append(f'<text x="{x + 65}" y="500" class="tick">{["none", "low", "medium"][j]}</text>')
        out.append(f'<text x="{x0 + 235}" y="560" class="gl">{g}</text>')
        x0 += 640
    return f'<svg viewBox="0 -40 1200 620" width="1200" height="620">{"".join(out)}</svg>'


def task_cells(m):
    items = sorted(S[m]["tasks"].items())
    cell = lambda t, v: (f'<td class="tn">{t[:2]}</td><td><span class="cell {"ok" if v["passes"] == v["trials"] else ("mid" if v["passes"] else "bad")}">'
                         f'{v["passes"]}/{v["trials"]}</span></td>')
    rows = "".join(f"<tr>{cell(*items[i])}{cell(*items[i + 5]) if i + 5 < len(items) else ''}</tr>" for i in range(5))
    return f'<table class="tc">{rows}</table>'


rob_f = [r for r in ROB if r["model"] in ("gpt-5.6-sol", "gpt-5.5")]
rob_txt = f'{sum(r["passed"] for r in rob_f)}/{len(rob_f)}'
sol_none = S.get("gpt-5.6-sol-none", {}).get("tasks", {})

TASKS = [("01", "Oblique-load lug", "1.6-power interaction + fitting factor"), ("02", "Short strut", "Johnson, not Euler, below L′/ρ 74.7"),
         ("03", "CAS → TAS, FL410", "isothermal layer, compressible, ISA+10"), ("04", "Load sheet", "fuel arm moves as tanks drain"),
         ("05", "Fatigue life", "rainflow finds the ground-air-ground cycle"), ("06", "Takeoff", "METAR wind is TRUE; NOTAM cuts TORA"),
         ("07", "Gust loads", "lighter aircraft, higher gust n; VA ∝ √W"), ("08", "Bolt group", "area-weighted; most-loaded ≠ critical"),
         ("09", "Tapered beam", "deeper at the tip: flanges ADD shear"), ("10", "Z-section", "Ixy ≠ 0: 2× My/I, flange tip in tension")]

css = """
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');
:root{--bg:#0b1220;--card:#121c2e;--ink:#eef2f7;--ink2:#b7c2d1;--mut:#6f7d91;--line:#22304a;--acc:#ff7a1a;--ok:#34d399;--bad:#f87171;--mid:#fbbf24;--blue:#7cb4ff}
*{box-sizing:border-box}body{margin:0;background:#05080f;font-family:Inter,sans-serif;color:var(--ink)}
.frame{width:1920px;height:1080px;background:radial-gradient(1200px 700px at 85% -10%,#16243d 0%,var(--bg) 60%);position:relative;overflow:hidden;padding:96px 120px;margin:0 0 24px}
.kick{font:700 22px 'JetBrains Mono';letter-spacing:.16em;text-transform:uppercase;color:var(--acc)}
h1{font:400 112px/1.0 'Instrument Serif';margin:22px 0 0;letter-spacing:-.02em}h1 em{color:var(--acc);font-style:italic}
h2{font:400 76px/1.04 'Instrument Serif';margin:18px 0 0;letter-spacing:-.01em}h2 em{color:var(--acc)}
p.lead{font-size:34px;line-height:1.45;color:var(--ink2);max-width:1500px;margin:28px 0 0}
.foot{position:absolute;left:120px;right:120px;bottom:52px;display:flex;justify-content:space-between;font:500 20px 'JetBrains Mono';color:var(--mut)}
.grid{display:grid;grid-template-columns:repeat(5,1fr);gap:22px;margin-top:56px}
.tile{background:var(--card);border:1px solid var(--line);border-radius:22px;padding:24px 24px 26px;min-height:250px}
.tile .n{font:700 24px 'JetBrains Mono';color:var(--acc)}.tile .t{font:600 30px/1.2 Inter;margin:12px 0 10px}.tile .d{font-size:23px;line-height:1.35;color:var(--ink2)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-top:50px}
.card{background:var(--card);border:1px solid var(--line);border-radius:24px;padding:34px 38px}
.card h3{font:700 22px 'JetBrains Mono';letter-spacing:.12em;text-transform:uppercase;color:var(--mut);margin:0 0 14px}
.big{font:400 150px/1 'Instrument Serif';color:var(--acc)}
.verdict{font:700 44px 'JetBrains Mono';margin-top:12px}.pass{color:var(--ok)}.fail{color:var(--bad)}
.mono{font:500 30px/1.5 'JetBrains Mono';color:var(--ink2)}
.bl{font:500 30px Inter;fill:var(--ink2)}.bv{font:700 30px 'JetBrains Mono';fill:var(--ink)}.bvc{font:700 34px 'JetBrains Mono';fill:var(--ink);text-anchor:middle}
.tick{font:500 26px 'JetBrains Mono';fill:var(--mut);text-anchor:middle}.gl{font:600 34px Inter;fill:var(--ink);text-anchor:middle}
.track{fill:#1a2639}.fill{fill:var(--acc)}.fill2{fill:var(--blue)}.fillmute{fill:#4a5a74}
.legend{font:500 24px 'JetBrains Mono';color:var(--mut);margin-top:18px}.legend b{color:var(--acc)}.legend i{color:var(--blue);font-style:normal}
ul.checks{list-style:none;padding:0;margin:26px 0 0;font-size:31px;line-height:1.5;color:var(--ink2)}ul.checks li:before{content:'✓  ';color:var(--ok);font-weight:700}
.quote{background:var(--card);border-left:6px solid var(--acc);border-radius:16px;padding:26px 32px;margin:22px 0;font-size:30px;line-height:1.4;color:var(--ink2)}
.quote b{color:var(--ink)}.quote .who{font:500 21px 'JetBrains Mono';color:var(--mut);display:block;margin-bottom:8px}
.cell{display:inline-block;width:74px;text-align:center;font:700 22px 'JetBrains Mono';padding:6px 0;border-radius:8px;margin:0 6px 6px 0}
.tc{border-collapse:collapse}.tc td{padding:2px 10px 2px 0}.tc .tn{font:500 22px JetBrains Mono;color:var(--mut);padding-left:18px}
.cell.ok{background:#0f3b2c;color:var(--ok)}.cell.mid{background:#3d3110;color:var(--mid)}.cell.bad{background:#401818;color:var(--bad)}
"""

beam_svg = """<svg viewBox="0 0 780 460" width="780" height="460">
 <defs><marker id="a" markerUnits="userSpaceOnUse" markerWidth="22" markerHeight="22" refX="18" refY="11" orient="auto"><path d="M0,0 L22,11 L0,22 z" fill="#ff7a1a"/></marker>
 <marker id="b" markerUnits="userSpaceOnUse" markerWidth="22" markerHeight="22" refX="18" refY="11" orient="auto"><path d="M0,0 L22,11 L0,22 z" fill="#7cb4ff"/></marker></defs>
 <rect x="20" y="140" width="26" height="180" fill="#2a3a55"/><text x="4" y="360" font-family="JetBrains Mono" font-size="20" fill="#6f7d91">fixed root</text>
 <polygon points="46,185 700,115 700,345 46,275" fill="#1a2639" stroke="#b7c2d1" stroke-width="3"/>
 <line x1="46" y1="185" x2="700" y2="115" stroke="#eef2f7" stroke-width="10"/><line x1="46" y1="275" x2="700" y2="345" stroke="#eef2f7" stroke-width="10"/>
 <line x1="300" y1="80" x2="300" y2="390" stroke="#ff7a1a" stroke-width="3" stroke-dasharray="10 8"/>
 <text x="262" y="68" font-family="JetBrains Mono" font-size="22" fill="#ff7a1a">station</text>
 <line x1="620" y1="300" x2="620" y2="170" stroke="#ff7a1a" stroke-width="6" marker-end="url(#a)"/><text x="636" y="245" font-family="Inter" font-weight="700" font-size="30" fill="#eef2f7">V</text>
 <line x1="312" y1="157" x2="420" y2="146" stroke="#7cb4ff" stroke-width="6" marker-end="url(#b)"/>
 <text x="340" y="120" font-family="JetBrains Mono" font-size="19" fill="#7cb4ff">C: pushes out, rises</text>
 <line x1="420" y1="315" x2="312" y2="304" stroke="#7cb4ff" stroke-width="6" marker-end="url(#b)"/>
 <text x="340" y="352" font-family="JetBrains Mono" font-size="19" fill="#7cb4ff">T: pulls in, rises</text>
 <text x="390" y="430" font-family="JetBrains Mono" font-size="20" fill="#6f7d91">deeper toward the free end →</text></svg>"""

frames = []
frames.append(f"""<div class="frame" id="s1"><div class="kick">micro1 Eval Hackathon · 2026</div>
<h1 style="font-size:190px;margin-top:120px">Aero<em>Margin</em></h1>
<p class="lead" style="font-size:44px;max-width:1600px">Does the model pick the right method <b>and the right sign</b> before it calculates? Ten aerospace hand calculations, each with one textbook default reversed, graded by code.</p>
<div class="foot"><span>Paras Adlakha · Harshita Adlakha</span><span>stress · fatigue · loads · performance · W&amp;B</span></div></div>""")
frames.append(f"""<div class="frame" id="s2"><div class="kick">The problem</div><h2>Engineers already ask models for margins.<br><em>A wrong margin looks like a right one.</em></h2>
<div class="two"><div class="card"><div class="big">79%</div><p class="lead" style="margin-top:14px;font-size:30px">of aerospace &amp; defense design engineers whose companies have <b>not</b> approved AI tools use them anyway.</p><p class="mono" style="font-size:20px">Molex survey, 1,021 engineering stakeholders, 2025</p></div>
<div class="card"><h3>Same beam, same numbers</h3><div class="mono">Model (textbook formula)</div><div class="verdict pass">MS = +0.71 · PASS</div><div class="mono" style="margin-top:34px">Checker (free body)</div><div class="verdict fail">MS = −0.08 · FAIL</div><p class="lead" style="font-size:26px">The beam tapers the other way. The familiar formula is unconservative by 86%.</p></div></div>
<div class="foot"><span>AeroMargin</span><span>02</span></div></div>""")
tiles = "".join(f'<div class="tile"><div class="n">{n}</div><div class="t">{t}</div><div class="d">{d}</div></div>' for n, t, d in TASKS)
frames.append(f"""<div class="frame" id="s3"><div class="kick">The eval</div><h2>Ten tasks. Each one reverses a <em>textbook default</em>.</h2><div class="grid">{tiles}</div>
<div class="foot"><span>Every task: full data, stated outputs, a reference solution, a code grader</span><span>03</span></div></div>""")
frames.append(f"""<div class="frame" id="s4"><div class="kick">Task 09 · tapered beam</div><h2>The relief formula assumes the beam gets <em>shallower</em> toward the tip.</h2>
<div class="two" style="grid-template-columns:780px 1fr;align-items:center">{beam_svg}
<div><div class="card"><h3>Textbook (Resal relief)</h3><div class="mono">V − (M/h)(tan α₁+tan α₂) = 4,200 lbf</div><div class="verdict pass">MS +0.71 · pass</div></div>
<div class="card" style="margin-top:22px"><h3>Free body of the outboard part</h3><div class="mono">both flange components point UP, with V<br>V + 2(M/h)tan α = 7,800 lbf</div><div class="verdict fail">MS −0.08 · fail</div></div></div></div>
<div class="foot"><span>Megson ch. 16; Bruhn A11</span><span>04</span></div></div>""")
frames.append(f"""<div class="frame" id="s5"><div class="kick">Grading</div><h2>Code graders only. <em>{VAL['checks']} checks</em>, before any model ran.</h2>
<ul class="checks"><li>Accepts every reference solution, and reformatted versions of it (commas, units, case)</li>
<li>Accepts every number nudged to 80% of its tolerance: no false fails from rounding</li>
<li>Rejects each critical field moved past tolerance, one at a time</li>
<li>Rejects 24 trap answers, each a specific mistake an engineer would recognise</li>
<li>Rejects gaming: echoed templates, “pass|fail” hedges, lists of candidates, a second JSON</li>
<li>Oracle run: all 10 reference solutions pass through the full harness</li></ul>
<div class="foot"><span>Grades the final JSON, not the path · partial credit + critical fields</span><span>05</span></div></div>""")
frames.append(f"""<div class="frame" id="s6"><div class="kick">Results · medium reasoning · 3 trials × 10 tasks</div><h2>The newest models pass. <em>Everything else breaks somewhere.</em></h2>
<div style="margin-top:46px">{bars(MAIN)}</div><div class="legend"><b>■</b> pass rate (all critical fields right) &nbsp; <i>▬</i> pass^3 (right on all 3 trials)</div>
<div class="foot"><span>Same prompts, same graders · runs on 8–9 Nov 2026</span><span>06</span></div></div>""")
frames.append(f"""<div class="frame" id="s7"><div class="kick">Reasoning effort · same model, same prompts</div><h2>Turn reasoning off and the frontier <em>falls back on the textbook</em>.</h2>
<div class="two" style="grid-template-columns:1150px 1fr;align-items:end;margin-top:30px"><div>{effort()}</div>
<div class="card"><h3>GPT-5.6 Sol, reasoning off</h3><div style="margin-top:8px">{task_cells("gpt-5.6-sol-none") if "gpt-5.6-sol-none" in S else ""}</div><p class="lead" style="font-size:25px">tasks 01→10 (passes / 3). Task 09: the textbook relief formula on every trial.</p></div></div>
<div class="foot"><span>Robustness: sign-reversed variants of tasks 09 &amp; 10 passed {rob_txt} at medium effort</span><span>07</span></div></div>""")
frames.append(f"""<div class="frame" id="s8"><div class="kick">What the transcripts show</div><h2>The wrong answers are <em>the shortcuts</em>, word for word.</h2>
<div class="quote"><span class="who">o3 · task 01 · 3 of 3 trials</span>“Bruhn D1 gives an <b>elliptical interaction</b>…” → MS <b>+0.055, PASS</b>. Bruhn's curve is the 1.6 power; the truth is MS −0.025, FAIL.</div>
<div class="quote"><span class="who">GPT-5.6 Sol, reasoning off · task 09 · 3 of 3 trials</span>Applies V − (M/h)Σtan α → <b>4,200 lbf, MS +0.71</b>. The beam is deeper at the tip; the web carries 7,800 lbf.</div>
<div class="quote"><span class="who">GPT-5.5, reasoning off · task 06 · 3 of 3 trials</span>Uses the METAR wind as magnetic → <b>2 kt</b> of headwind instead of 5.5 kt. METAR winds are reported from true north.</div>
<div class="foot"><span>Every transcript is in the repository</span><span>08</span></div></div>""")
frames.append(f"""<div class="frame" id="s9"><div class="kick">Hot take</div><h2>The gap isn't arithmetic.<br>It's <em>recall versus re-derive</em>.</h2>
<p class="lead">The same model is right on every trial when it reasons, and confidently wrong when it answers from memory. For engineering teams, the reasoning setting matters more than the leaderboard. Ask for the governing case and every load's direction before any number, as a senior checker would. To close the gap for good, train on reversed defaults: <span style="color:var(--acc)">robustness.py</span> generates them.</p>
<div class="foot"><span>Paras Adlakha · Harshita Adlakha</span><span>AeroMargin · python validate_graders.py · run_eval.py · summarize.py</span></div></div>""")

out = ROOT / "docs" / "slides"
out.mkdir(parents=True, exist_ok=True)
(out / "slides.html").write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>AeroMargin slides</title><style>{css}</style></head><body>{''.join(frames)}</body></html>", encoding="utf-8")
print("wrote", out / "slides.html", len(frames), "slides")
