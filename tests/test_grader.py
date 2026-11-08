"""Unit tests for the grader, the reference solutions and the harness plumbing. Standard library only.
    python -m unittest discover -s tests -v
"""
import json
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from graders.grader import check_field, extract_answer, grade, load_task, task_ids, to_bool, to_enum, to_number  # noqa: E402
from graders.traps import traps_for  # noqa: E402
import robustness  # noqa: E402


def wrap(d):
    return "work\n```json\n" + json.dumps(d) + "\n```"


class Parsing(unittest.TestCase):
    def test_last_fenced_block_wins(self):
        t = "```json\n{\"a\": 1}\n```\nlater\n```json\n{\"a\": 2}\n```"
        self.assertEqual(extract_answer(t), {"a": 2})

    def test_bare_object_fallback(self):
        self.assertEqual(extract_answer('final: {"x": "y", "n": {"k": 1}}'), {"x": "y", "n": {"k": 1}})

    def test_braces_inside_strings(self):
        self.assertEqual(extract_answer('{"s": "a } b", "v": 3}'), {"s": "a } b", "v": 3})

    def test_no_answer(self):
        self.assertIsNone(extract_answer("no json here"))
        self.assertIsNone(extract_answer(""))


class Normalising(unittest.TestCase):
    def test_numbers(self):
        self.assertEqual(to_number("1,330"), 1330.0)
        self.assertEqual(to_number("−0.08"), -0.08)
        self.assertEqual(to_number("2,655 ft"), 2655.0)
        self.assertIsNone(to_number(True))
        self.assertIsNone(to_number(float("nan")))
        self.assertIsNone(to_number("about 5"))

    def test_enums_reject_hedges(self):
        self.assertEqual(to_enum(" FAIL. "), "fail")
        self.assertEqual(to_enum("lug oblique"), "lug_oblique")
        self.assertIsNone(to_enum("pass|fail"))
        self.assertIsNone(to_enum("pass/fail"))
        self.assertIsNone(to_enum(["fail"]))

    def test_bools(self):
        self.assertIs(to_bool("False"), False)
        self.assertIs(to_bool(True), True)
        self.assertIsNone(to_bool("no"))

    def test_tolerances(self):
        rule = {"type": "number", "tol_abs": 0.01}
        self.assertTrue(check_field(rule, -0.0251, -0.017)[0])
        self.assertFalse(check_field(rule, -0.0251, 0.055)[0])
        rel = {"type": "number", "tol_rel": 0.01}
        self.assertTrue(check_field(rel, 7800, 7870)[0])
        self.assertFalse(check_field(rel, 7800, 4200)[0])


class Tasks(unittest.TestCase):
    def test_ten_tasks_with_all_parts(self):
        ids = task_ids()
        self.assertEqual(len(ids), 10)
        for t in ids:
            d = ROOT / "tasks" / t
            for f in ("instruction.md", "instruction_guided.md", "solution.py", "task.json"):
                self.assertTrue((d / f).exists(), f"{t}/{f}")

    def test_every_graded_key_is_named_in_both_prompts(self):
        for t in task_ids():
            for variant in ("realistic", "guided"):
                task = load_task(t, variant)
                for key in task["fields"]:
                    self.assertIn(f'"{key}"', task["instruction"], f"{t} ({variant}) prompt does not name {key}")

    def test_reference_passes_and_every_task_has_a_critical_field(self):
        for t in task_ids():
            task = load_task(t)
            ref = {k: task["reference"][k] for k in task["fields"]}
            g = grade(task, wrap(ref))
            self.assertTrue(g["passed"], t)
            self.assertEqual(g["score"], 1.0, t)
            self.assertTrue(any(r.get("critical") for r in task["fields"].values()), t)

    def test_every_trap_fails(self):
        for t in task_ids():
            task = load_task(t)
            traps = traps_for(t)
            self.assertGreaterEqual(len(traps), 1, t)
            for label, ans in traps.items():
                self.assertFalse(grade(task, wrap(ans))["passed"], f"{t}: trap '{label}' passed")

    def test_references_carry_no_answer_into_prompts(self):
        # the reference numbers must not appear in the prompt (no answer leakage)
        leaks = {"01": "-0.025", "02": "23582", "05": "97158", "06": "2655", "09": "7800", "10": "22222"}
        for t in task_ids():
            key = leaks.get(t[:2])
            if key:
                self.assertNotIn(key, load_task(t)["instruction"].replace(",", ""), t)


class EngineeringChecks(unittest.TestCase):
    """Independent hand-style re-derivations of key reference numbers."""

    def test_lug_interaction(self):
        pu = 15000 * 1.5 * 1.15
        ra, rt = pu * math.cos(math.radians(40)) / 38000, pu * math.sin(math.radians(40)) / 21000
        self.assertAlmostEqual((ra ** 1.6 + rt ** 1.6) ** (-1 / 1.6) - 1, load_task("01-oblique-lug-fitting")["reference"]["ms_lug_oblique"], places=3)

    def test_tapered_web(self):
        self.assertAlmostEqual(6000 + 2 * (180000 / 6.0) * 0.03, 7800.0)

    def test_z_section_properties(self):
        r = load_task("10-z-section-unsymmetric-bending")["reference"]
        self.assertAlmostEqual(r["ix_in4"], 0.1 * 27 / 12 + 2 * 0.1 * 2.25, places=4)
        self.assertAlmostEqual(r["ixy_in4"], 0.15, places=4)
        self.assertGreater(r["stress_A_psi"], 0)   # the 'compressed' flange tip is in tension

    def test_robustness_variants_mirror_symmetry(self):
        z = {v["id"]: v["ref"] for v in robustness.z_variants()}
        self.assertAlmostEqual(z["zsec-topright-comptop"]["stress_A_psi"], z["zsec-topleft-comptop"]["stress_A_psi"])


if __name__ == "__main__":
    unittest.main()
