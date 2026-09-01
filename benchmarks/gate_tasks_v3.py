#!/usr/bin/env python3
"""Prove the tier-v3 fixtures do what the design claims. No model, $0.

    python benchmarks/gate_tasks_v3.py

Same three checks as the v2 gate - BROKEN, SOLVABLE, TRAP - plus one that only
means anything once a fixture spans several files:

  CROSS-FILE  the decoy must not touch the file the reference solution had to
              change. If the plausible fix edits the same module as the real
              fix, the fixture is testing edge-case reasoning, not
              symptom-versus-cause, and it belongs at v2 instead.

Fixtures are multi-file, so solution/ and decoy/ are directories overlaid on a
copy of workspace/ rather than single files.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
TASKS = ROOT / "tasks_v3"


def run_with(task: pathlib.Path, overlay: str | None,
             files: list[str]) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        wd = pathlib.Path(tmp) / "ws"
        shutil.copytree(task / "workspace", wd)
        if overlay:
            for f in sorted((task / overlay).iterdir()):
                shutil.copy(f, wd / f.name)
        shutil.copy(task / "test_hidden.py", wd / "test_hidden.py")
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", *files],
                           cwd=wd, capture_output=True, text=True, timeout=120)
        return p.returncode == 0


def main() -> int:
    if not TASKS.is_dir():
        print("no tasks_v3/ - run: python benchmarks/make_tasks_v3.py",
              file=sys.stderr)
        return 2

    fails, traps, checked = [], 0, 0
    print(f"{'fixture':<24}{'BROKEN':<9}{'SOLVABLE':<11}{'TRAP':<22}CROSS-FILE")
    print("-" * 76)

    for d in sorted(TASKS.iterdir()):
        if not (d / "task.json").exists():
            continue
        checked += 1

        broken = not run_with(d, None, ["test_src.py"])
        solvable = run_with(d, "solution", ["test_src.py", "test_hidden.py"])
        decoy_visible = run_with(d, "decoy", ["test_src.py"])
        decoy_hidden = run_with(d, "decoy", ["test_hidden.py"])
        trap_ok = decoy_visible and not decoy_hidden
        trap = "ok" if trap_ok else ("decoy fails visible" if not decoy_visible
                                     else "decoy PASSES hidden")
        if trap_ok:
            traps += 1

        sol_files = {f.name for f in (d / "solution").iterdir()}
        dec_files = {f.name for f in (d / "decoy").iterdir()}
        # The file the real fix HAD to change, that the decoy leaves alone.
        cause = sol_files - dec_files
        cross_ok = bool(cause)
        cross = ",".join(sorted(cause)) if cross_ok else "SAME FILES"

        print(f"{d.name:<24}{'ok' if broken else 'FAIL':<9}"
              f"{'ok' if solvable else 'FAIL':<11}{trap:<22}{cross}")

        for label, ok in (("BROKEN", broken), ("SOLVABLE", solvable),
                          ("TRAP", trap_ok), ("CROSS-FILE", cross_ok)):
            if not ok:
                fails.append(f"{d.name}: {label}")

    print("-" * 76)
    print(f"{checked} fixtures · {traps} verified traps · "
          f"CROSS-FILE names the module the decoy never opens")

    if fails:
        print(f"\n{len(fails)} GATE FAILURES - do not run the sweep:")
        for f in fails:
            print(f"  {f}")
        return 1
    print("\nall gates pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
