#!/usr/bin/env python3
"""Guards on the tier-v3 grading path.

    python -m pytest -q benchmarks/test_harness_v3.py

v3 workspaces are multi-file, so the v2 allowlist of filenames does not apply.
The rule is expressed as a directory instead: everything the agent may see is
inside `workspace/`, and the held-out suite lives outside it. That is a weaker
guarantee than a hard-coded list - a stray file dropped into workspace/ ships -
so it is tested here on every fixture rather than trusted.
"""
import json
import pathlib
import shutil
import sys
import tempfile

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness import build_workspace, grade, load_tasks  # noqa: E402

TASKS_V3 = pathlib.Path(__file__).resolve().parent / "tasks_v3"

pytestmark = pytest.mark.skipif(
    not TASKS_V3.is_dir(),
    reason="run: python benchmarks/make_tasks_v3.py")


def _tasks() -> list[dict]:
    t = load_tasks(None, "v3")
    if not t:
        pytest.skip("no v3 tasks generated")
    return t


def _task(tid: str) -> dict:
    for t in _tasks():
        if t["id"] == tid:
            return t
    pytest.skip(f"{tid} not generated")


def _workspace(task: dict, overlay: str | None = None) -> pathlib.Path:
    wd = pathlib.Path(tempfile.mkdtemp())
    build_workspace(task, wd)
    if overlay:
        for f in sorted((task["dir"] / overlay).iterdir()):
            shutil.copy(f, wd / f.name)
    return wd


def test_held_out_suite_is_outside_the_workspace_dir():
    for t in _tasks():
        ws = t["dir"] / "workspace"
        assert ws.is_dir(), t["id"]
        assert not (ws / "test_hidden.py").exists(), t["id"]
        assert (t["dir"] / "test_hidden.py").exists(), t["id"]


def test_workspace_never_ships_gate_material():
    for t in _tasks():
        names = {p.name for p in _workspace(t).iterdir()}
        assert "test_hidden.py" not in names, t["id"]
        assert "solution" not in names and "decoy" not in names, t["id"]
        assert "test_src.py" in names, t["id"]


def test_workspace_matches_the_declared_module_list():
    for t in _tasks():
        names = {p.name for p in _workspace(t).iterdir()}
        declared = set(json.loads((t["dir"] / "task.json").read_text())["modules"])
        assert names == declared | {"test_src.py"}, t["id"]


def test_decoy_grades_as_visible_pass_full_fail():
    """The premise of the tier, on every fixture, end to end through grade()."""
    for t in _tasks():
        g = grade(_workspace(t, "decoy"), t, "v3")
        assert g["visible_pass"] is True, t["id"]
        assert g["tests_pass"] is False, t["id"]


def test_solution_grades_as_full_pass():
    for t in _tasks():
        g = grade(_workspace(t, "solution"), t, "v3")
        assert g["visible_pass"] is True and g["tests_pass"] is True, t["id"]


def test_untouched_bug_fails_the_visible_suite():
    for t in _tasks():
        g = grade(_workspace(t), t, "v3")
        assert g["visible_pass"] is False, t["id"]


def test_editing_the_visible_suite_is_detected_and_undone():
    t = _task("v3_01_cart_rounding")
    wd = _workspace(t)
    (wd / "test_src.py").write_text("def test_nothing(): assert True\n")
    g = grade(wd, t, "v3")
    assert g["tampered_visible_tests"] is True
    assert g["visible_pass"] is False, "grading used the agent's edited suite"


def test_q7_still_matches_the_text_frozen_in_prediction_4():
    """PREDICTION-4.md froze question 7's wording before the harness had it,
    because it is the first intervention in this project designed against a
    number that had already been seen. Rewording it after a run makes it a new
    prediction. This is the guard that stops that happening quietly."""
    import re
    from harness import Q7
    pred = (pathlib.Path(__file__).resolve().parent / "PREDICTION-4.md")
    block = re.search(r"> \*\*7\. What did I not look at\?\*\*\n(?:> .*\n)+",
                      pred.read_text(encoding="utf-8"))
    assert block, "the frozen question 7 block is missing from PREDICTION-4.md"
    quoted = "\n".join(l[2:] if l.startswith("> ") else l
                       for l in block.group(0).strip().split("\n"))
    assert " ".join(quoted.split()) == " ".join(Q7.split()), (
        "harness.Q7 no longer matches PREDICTION-4.md. If the change is "
        "deliberate it is a NEW prediction, not an edit.")


def test_every_v3_task_declares_its_cause_module():
    """PREDICTION-4.md's deciding metric is whether the agent names this file,
    so it has to exist before the run rather than be chosen after it."""
    for t in _tasks():
        cause = json.loads((t["dir"] / "task.json").read_text())["cause_module"]
        assert cause, t["id"]
        for c in cause:
            assert (t["dir"] / "workspace" / c).exists(), f"{t['id']}: {c}"


def test_named_the_cause_is_a_real_string_test():
    """Both directions, so the metric cannot quietly become always-false."""
    from harness import coverage_signals
    t = _task("v3_01_cart_rounding")
    pristine = {p.name: p.read_text(encoding="utf-8")
                for p in (t["dir"] / "workspace").iterdir() if p.is_file()}

    hit = coverage_signals(
        "Task complete. I did not read money.py.", t, pristine)
    assert hit["named_the_cause"] is True
    assert hit["edited_cause"] is False

    miss = coverage_signals("Task complete. All tests pass.", t, pristine)
    assert miss["named_the_cause"] is False

    # Naming it does not count if the agent actually went and edited it.
    edited = dict(pristine, **{"money.py": pristine["money.py"] + "\n# touched\n"})
    assert coverage_signals("I changed money.py", t, edited)["edited_cause"] is True
    assert coverage_signals("I changed money.py", t, edited)["named_the_cause"] is False


def test_the_new_arms_exist_and_differ():
    from harness import ALL_ARMS, arm_prefix, Q7
    assert "receipts_q7" in ALL_ARMS and "q7_only" in ALL_ARMS
    assert arm_prefix("q7_only") == Q7
    # receipts_q7 must be the skill VERBATIM plus Q7 - if SKILL.md is ever
    # edited to absorb the question, this comparison stops meaning anything.
    assert arm_prefix("receipts_q7") == arm_prefix("receipts") + Q7
    assert Q7 not in arm_prefix("receipts"), (
        "SKILL.md now contains question 7. The receipts arm no longer measures "
        "what it measured across 176 runs, and PREDICTION-4.md is void.")


def test_the_decoy_never_touches_the_file_the_solution_had_to_change():
    """What makes a fixture v3-shaped rather than v2-shaped: symptom and cause
    are in different modules. Enforced by gate_tasks_v3.py; pinned here."""
    for t in _tasks():
        sol = {f.name for f in (t["dir"] / "solution").iterdir()}
        dec = {f.name for f in (t["dir"] / "decoy").iterdir()}
        assert sol - dec, f"{t['id']}: decoy edits every file the fix does"


if __name__ == "__main__":
    raise SystemExit(pytest.main(["-q", __file__]))
