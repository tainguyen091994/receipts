#!/usr/bin/env python3
"""What is half-finished, and the exact line to finish it. No model, $0.

    python benchmarks/resume.py            # status of every sweep
    python benchmarks/resume.py --run      # actually resume the newest one

A Pro plan has a rolling 5-hour window. A sweep that outlives it does not fail
loudly - the agent calls start erroring, and an errored run arrives carrying
tests_pass=False, which reads as "the agent could not fix it". The harness
aborts after 3 consecutive errors for exactly that reason, and excludes errored
runs from its table.

What it cannot do is remember your flags for you. `--resume STAMP` on its own
will happily resume a v3 sweep as a v1 sweep and print one table built from two
different instruments. So every sweep writes a manifest next to its runs, and
this reads it back.
"""
import argparse
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
RUNS = ROOT / "runs"


def sweeps() -> list[dict]:
    out = []
    for m in sorted(RUNS.glob("*.manifest.json")):
        try:
            man = json.loads(m.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        stamp = man["stamp"]
        done, errored = 0, 0
        for arm in man["arms"]:
            for tid in man["tasks"]:
                for r in range(man["runs"]):
                    f = RUNS / f"{stamp}_{arm}_{tid}_{r}.json"
                    if not f.exists():
                        continue
                    try:
                        rec = json.loads(f.read_text(encoding="utf-8"))
                    except json.JSONDecodeError:
                        continue
                    if rec.get("error"):
                        errored += 1
                    else:
                        done += 1
        man["_total"] = len(man["arms"]) * len(man["tasks"]) * man["runs"]
        man["_done"] = done
        man["_errored"] = errored
        man["_missing"] = man["_total"] - done - errored
        out.append(man)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true",
                    help="execute the resume command for the newest incomplete "
                         "sweep instead of only printing it")
    ap.add_argument("--stamp", help="act on this stamp rather than the newest")
    args = ap.parse_args()

    all_sweeps = sweeps()
    if not all_sweeps:
        print("no sweep manifests in benchmarks/runs/.\n"
              "Sweeps started before manifests existed can still be resumed by "
              "hand:\n  --resume <stamp>  with the SAME --tier and --tasks.")
        return 0

    print(f"{'stamp':<26}{'tier':<6}{'done':>6}{'err':>5}{'todo':>6}{'total':>7}"
          f"  model")
    print("-" * 74)
    for m in all_sweeps:
        flag = "" if m["_missing"] == 0 and m["_errored"] == 0 else "  <- unfinished"
        print(f"{m['stamp']:<26}{m['tier']:<6}{m['_done']:>6}{m['_errored']:>5}"
              f"{m['_missing']:>6}{m['_total']:>7}  {m['model'] or 'CLI default'}"
              f"{flag}")

    unfinished = [m for m in all_sweeps
                  if (m["_missing"] or m["_errored"]) and not m["dry_run"]]
    if args.stamp:
        unfinished = [m for m in unfinished if m["stamp"] == args.stamp] or \
                     [m for m in all_sweeps if m["stamp"] == args.stamp]
    if not unfinished:
        print("\nnothing to resume.")
        return 0

    target = unfinished[-1]
    todo = target["_missing"] + target["_errored"]
    print(f"\nnewest unfinished: {target['stamp']}  "
          f"({todo} of {target['_total']} runs still to do)")
    print("\nresume with:\n")
    print(f"  {target['resume_cmd']}\n")
    print("Resuming re-runs the errored cells and skips the good ones, so it "
          "costs\nonly the runs that are actually missing. Check the window "
          "first:\n\n  claude auth status\n")

    if args.run:
        print(f"running: {target['resume_cmd']}\n")
        return subprocess.run(target["resume_cmd"].split(), cwd=REPO).returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
