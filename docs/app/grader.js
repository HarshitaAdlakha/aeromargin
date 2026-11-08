// JavaScript port of graders/grader.py, used by the live mode of the explorer.
// Parity with the Python grader is checked on every saved transcript by tests/grader_parity.mjs.

function lastObject(text) {
  let found = null, depth = 0, start = -1, inStr = false, esc = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (inStr) {
      if (esc) esc = false;
      else if (ch === '\\') esc = true;
      else if (ch === '"') inStr = false;
      continue;
    }
    if (ch === '"' && depth > 0) inStr = true;
    else if (ch === '{') { if (depth === 0) start = i; depth++; }
    else if (ch === '}' && depth > 0) {
      depth--;
      if (depth === 0) { try { found = JSON.parse(text.slice(start, i + 1)); } catch { /* not JSON */ } }
    }
  }
  return found;
}

const isObj = (o) => o !== null && typeof o === 'object' && !Array.isArray(o);

export function extractAnswer(text) {
  if (!text) return null;
  const blocks = [...text.matchAll(/```(?:json|JSON)?\s*(\{[\s\S]*?\})\s*```/g)].map((m) => m[1]);
  for (const b of blocks.reverse()) {
    try { const o = JSON.parse(b); if (isObj(o)) return o; } catch { const o = lastObject(b); if (isObj(o)) return o; }
  }
  const o = lastObject(text);
  return isObj(o) ? o : null;
}

export function toNumber(v) {
  if (typeof v === 'boolean' || v === null || v === undefined) return null;
  if (typeof v === 'number') return Number.isFinite(v) ? v : null;
  if (typeof v === 'string') {
    let s = v.trim().replaceAll(',', '').replaceAll('−', '-');
    s = s.replace(/\s*(lbf|lb|psi|ksi|kt|kts|keas|ft|in|pa|k|%|flights)$/i, '');
    if (/^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$/.test(s)) return parseFloat(s);
  }
  return null;
}

export function toEnum(v) {
  if (typeof v !== 'string') return null;
  let s = v.trim().replace(/^\.+|\.+$/g, '').trim().toLowerCase().replaceAll('-', '_').replaceAll(' ', '_');
  if (/[|/,]/.test(s)) return null;
  return s;
}

export function toBool(v) {
  if (typeof v === 'boolean') return v;
  if (typeof v === 'string' && ['true', 'false'].includes(v.trim().toLowerCase())) return v.trim().toLowerCase() === 'true';
  return null;
}

export function checkField(rule, want, got) {
  if (rule.type === 'number') {
    const g = toNumber(got);
    if (g === null) return [false, `not a number: ${JSON.stringify(got)}`];
    const w = Number(want);
    const tol = Math.max(rule.tol_abs || 0, (rule.tol_rel || 0) * Math.abs(w));
    return [Math.abs(g - w) <= tol + 1e-12, `got ${g}, want ${w} ± ${+tol.toPrecision(6)}`];
  }
  if (rule.type === 'enum') {
    const g = toEnum(got);
    const acc = (rule.accept || [want]).map((a) => String(a).toLowerCase());
    return [acc.includes(g), `got ${JSON.stringify(got)}, want one of ${JSON.stringify(acc)}`];
  }
  if (rule.type === 'bool') {
    const g = toBool(got);
    return [g !== null && g === Boolean(want), `got ${JSON.stringify(got)}, want ${want}`];
  }
  throw new Error(rule.type);
}

// task = { fields: {name: rule}, reference: {name: value} }
export function grade(task, text) {
  const ans = extractAnswer(text);
  const fields = {};
  if (!ans) {
    for (const k of Object.keys(task.fields)) fields[k] = { ok: false, why: 'no JSON answer found' };
    return { parsed: false, score: 0, passed: false, fields, answer: null };
  }
  let num = 0, den = 0, passed = true;
  for (const [name, rule] of Object.entries(task.fields)) {
    const [ok, why] = name in ans ? checkField(rule, task.reference[name], ans[name]) : [false, 'missing'];
    const w = rule.weight ?? 1;
    den += w; if (ok) num += w;
    if (rule.critical && !ok) passed = false;
    fields[name] = { ok, why, critical: !!rule.critical };
  }
  return { parsed: true, score: Math.round((num / den) * 1e4) / 1e4, passed, fields, answer: ans };
}
