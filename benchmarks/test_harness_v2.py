#!/usr/bin/env python3
"""Guards on the tier-v2 grading path.

    python -m pytest -q benchmarks/test_harness_v2.py

The tier is worth exactly as much as the held-out file being genuinely held out.
One stray copy in the workspace and every v2 number silently becomes a v1
number - passing, plausible, and meaningless. That is the failure this file
exists to prevent, so it is tested rather than asserted in a comment.
"""
import json
import pathlib
import shutil
import sys
import tempfile

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness import WORKSPACE_FILES, grade, load_tasks  # noqa: E402

TASKS_V2 = pathlib.Path(__file__).resolve().parent / "tasks_v2"

pytestmark = pytest.mark.skipif(
    not TASKS_V2.is_dir(),
    reason="run: python benchmarks/make_tasks_v2.py")


def _task(tid: str) -> dict:
    for t in load_tasks([tid], "v2"):
        return t
    pytest.skip(f"{tid} not generated")


def _workspace(task: dict, impl: str | None = None) -> pathlib.Path:
    """Build a workspace exactly the way the harness builds one."""
    wd = pathlib.Path(tempfile.mkdtemp())
    for f in WORKSPACE_FILES:
        shutil.copy(task["dir"] / f, wd / f)
    if impl:
        shutil.copy(task["dir"] / impl, wd / "src.py")
    return wd


def test_workspace_never_ships_the_held_out_file():
    for leak in ("test_hidden.py", "solution.py", "decoy.py"):
        assert leak not in WORKSPACE_FILES


def test_workspace_contents_are_exactly_two_files():
    wd = _workspace(_task("t11_int_div"))
    assert sorted(p.name for p in wd.iterdir()) == ["src.py", "test_src.py"]


def test_every_v2_task_has_a_hidden_suite():
    tasks = load_tasks(None, "v2")
    assert tasks, "no v2 tasks generated"
    for t in tasks:
        assert (t["dir"] / "test_hidden.py").exists(), t["id"]
        assert (t["dir"] / "solution.py").exists(), t["id"]
        assert json.loads((t["dir"] / "task.json").read_text())["tier"] == "v2"


def test_decoy_grades_as_visible_pass_full_fail():
    """The tier's whole premise, end to end through grade()."""
    task = _task("t11_int_div")
    wd = _workspace(task, "decoy.py")
    g = grade(wd, task, "v2")
    assert g["visible_pass"] is True
    assert g["tests_pass"] is False
    assert g["tampered_visible_tests"] is False


def test_solution_grades_as_full_pass():
    task = _task("t11_int_div")
    g = grade(_workspace(task, "solution.py"), task, "v2")
    assert g["visible_pass"] is True and g["tests_pass"] is True


def test_untouched_bug_fails_both():
    task = _task("t11_int_div")
    g = grade(_workspace(task), task, "v2")
    assert g["visible_pass"] is False and g["tests_pass"] is False


def test_editing_the_visible_suite_is_detected_and_undone():
    """An agent that deletes the failing test does not get a green run."""
    task = _task("t11_int_div")
    wd = _workspace(task)
    (wd / "test_src.py").write_text("def test_nothing(): assert True\n")
    g = grade(wd, task, "v2")
    assert g["tampered_visible_tests"] is True
    assert g["visible_pass"] is False, "grading used the agent's edited suite"
    assert g["tests_pass"] is False


if __name__ == "__main__":
    raise SystemExit(pytest.main(["-q", __file__]))
