// Checks that the browser grader (docs/app/grader.js) gives exactly the same verdicts and scores as
// graders/grader.py on every saved transcript and on every validation case.
//   python tests/dump_parity_cases.py && node tests/grader_parity.mjs
import { readFileSync } from 'node:fs';
import { grade } from '../docs/app/grader.js';

const cases = JSON.parse(readFileSync(new URL('./parity_cases.json', import.meta.url), 'utf8'));
let bad = 0;
for (const c of cases) {
  const g = grade(c.task, c.text);
  const same = g.passed === c.py.passed && Math.abs(g.score - c.py.score) < 1e-9 &&
    Object.keys(c.py.fields).every((k) => g.fields[k].ok === c.py.fields[k]);
  if (!same) { bad++; if (bad <= 5) console.log('MISMATCH', c.id, { js: [g.passed, g.score], py: [c.py.passed, c.py.score] }); }
}
console.log(`${cases.length} cases, ${bad} mismatches`);
process.exit(bad ? 1 : 0);
