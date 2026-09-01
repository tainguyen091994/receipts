#!/usr/bin/env python3
"""Prove the tier-v2 fixtures do what the design claims. No model, $0.

    python benchmarks/gate_tasks_v2.py

Three checks per fixture, each of which can fail the whole tier:

  BROKEN    the visible suite must FAIL against the shipped src.py.
            Otherwise the agent is handed a green suite and there is nothing
            to fix - the run measures nothing.

  SOLVABLE  the reference solution.py must PASS visible + hidden.
            A hidden test no correct fix can satisfy would make false-success
            unavoidable, which would make the metric meaningless in the
            flattering direction: every arm looks like a liar.

  TRAP      where a decoy.py exists, the plausible-but-wrong fix must PASS the
            visible suite and FAIL the hidden suite.
            This is the whole premise of the tier. Without it, "hidden tests"
            is just "more tests", and the agent that iterates to green on the
            visible suite is also green on the hidden one.

Fixtures with no decoy are reported as `-`. They are not defects; not every bug
has a plausible near-miss. But the count of real traps is the honest measure of
how much this tier can actually detect, so it is printed at the end and belongs
in any write-up of the results.
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
TASKS = ROOT / "tasks_v2"


def pytest_in(workdir: pathlib.Path, files: list[str]) -> bool:
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", *files],
                       cwd=workdir, capture_output=True, text=True, timeout=120)
    return p.returncode == 0


def run_with(task: pathlib.Path, impl: str, files: list[str]) -> bool:
    """Copy the fixture into a temp dir with `impl` standing in for src.py."""
    with tempfile.TemporaryDirectory() as tmp:
        wd = pathlib.Path(tmp)
        shutil.copy(task / impl, wd / "src.py")
        shutil.copy(task / "test_src.py", wd / "test_src.py")
        shutil.copy(task / "test_hidden.py", wd / "test_hidden.py")
        return pytest_in(wd, files)


def main() -> int:
    if not TASKS.is_dir():
        print("no tasks_v2/ - run: python benchmarks/make_tasks_v2.py",
              file=sys.stderr)
        return 2

    fails, traps, checked = [], 0, 0
    print(f"{'fixture':<24}{'BROKEN':<9}{'SOLVABLE':<11}{'TRAP':<8}")
    print("-" * 52)

    for d in sorted(TASKS.iterdir()):
        if not (d / "task.json").exists():
            continue
        checked += 1

        broken = not run_with(d, "src.py", ["test_src.py"])
        solvable = run_with(d, "solution.py", ["test_src.py", "test_hidden.py"])

        if (d / "decoy.py").exists():
            decoy_visible = run_with(d, "decoy.py", ["test_src.py"])
            decoy_hidden = run_with(d, "decoy.py", ["test_hidden.py"])
            trap_ok = decoy_visible and not decoy_hidden
            if trap_ok:
                traps += 1
                trap = "ok"
            else:
                trap = ("decoy fails visible" if not decoy_visible
                        else "decoy PASSES hidden")
        else:
            trap = "-"
            trap_ok = True

        print(f"{d.name:<24}{'ok' if broken else 'FAIL':<9}"
              f"{'ok' if solvable else 'FAIL':<11}{trap:<8}")

        for label, ok in (("BROKEN", broken), ("SOLVABLE", solvable),
                          ("TRAP", trap_ok)):
            if not ok:
                fails.append(f"{d.name}: {label}")

    print("-" * 52)
    print(f"{checked} fixtures · {traps} verified traps "
          f"(decoy passes visible, fails hidden)")

    if fails:
        print(f"\n{len(fails)} GATE FAILURES - do not run the sweep:")
        for f in fails:
            print(f"  {f}")
        return 1
    print("\nall gates pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
