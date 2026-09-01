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


def test_the_decoy_never_touches_the_file_the_solution_had_to_change():
    """What makes a fixture v3-shaped rather than v2-shaped: symptom and cause
    are in different modules. Enforced by gate_tasks_v3.py; pinned here."""
    for t in _tasks():
        sol = {f.name for f in (t["dir"] / "solution").iterdir()}
        dec = {f.name for f in (t["dir"] / "decoy").iterdir()}
        assert sol - dec, f"{t['id']}: decoy edits every file the fix does"


if __name__ == "__main__":
    raise SystemExit(pytest.main(["-q", __file__]))
