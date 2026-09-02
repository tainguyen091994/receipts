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
import collections
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
RUNS = ROOT / "runs"
STAMP_RE = re.compile(r"^((?:dryrun-)?\d{4}-\d{2}-\d{2}-\d{6})_"
                      r"([a-z]+)_(.+)_(\d+)\.json$")


def orphans() -> dict:
    """Sweeps whose run files exist but whose manifest does not.

    Manifests were added after three sweeps had already run, and the first
    thing that needed resuming was one of them - a contingency that did not
    cover the case it was built for. Reconstruct what the run files can prove:
    stamp, tier, arms, tasks, repeats. The model is NOT recoverable from a run
    record, so --adopt asks for it rather than guessing.
    """
    have = {json.loads(m.read_text(encoding="utf-8"))["stamp"]
            for m in RUNS.glob("*.manifest.json")}
    found = collections.defaultdict(
        lambda: {"arms": set(), "tasks": set(), "runs": 0, "tier": set(),
                 "done": 0, "errored": 0})
    for f in sorted(RUNS.glob("*.json")):
        m = STAMP_RE.match(f.name)
        if not m or m.group(1) in have:
            continue
        stamp, arm, task, r = m.groups()
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if "final" not in rec:
            continue
        o = found[stamp]
        o["arms"].add(arm)
        o["tasks"].add(task)
        o["runs"] = max(o["runs"], int(r) + 1)
        o["tier"].add(rec.get("tier", "v1"))
        o["errored" if rec.get("error") else "done"] += 1
    return found


def window_is_open(model: str) -> bool:
    """Ask the model one trivial question and see whether it answers.

    `claude auth status` reports login and plan, NOT whether the rolling
    5-hour window has room - it says subscriptionType: pro just as happily
    while every call is being refused. The only honest check is a call.
    """
    sys.path.insert(0, str(ROOT))
    from harness import CLAUDE_BIN  # noqa: E402
    cmd = [CLAUDE_BIN, "-p", "reply with the single word: ok",
           "--output-format", "json"]
    if model:
        cmd += ["--model", model]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as e:
        print(f"  probe could not run: {e}")
        return False
    if p.returncode == 0:
        print("  window is OPEN - one probe call succeeded.")
        return True
    blob = (p.stdout + p.stderr).strip()
    print(f"  window still CLOSED (exit {p.returncode}).")
    if blob:
        print(f"  {blob[:300]}")
    else:
        print("  the CLI said nothing at all, which is what a filled Pro "
              "window looks like from here. Try again later.")
    return False


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
    ap.add_argument("--adopt", metavar="STAMP",
                    help="write a manifest for a sweep that has run files but "
                         "no manifest, reconstructing tier/arms/tasks/runs from "
                         "the files. Needs --model, which a run record does not "
                         "store")
    ap.add_argument("--model", default="",
                    help="model id, for --adopt and for --check")
    ap.add_argument("--check", action="store_true",
                    help="spend one trivial call to find out whether the usage "
                         "window has actually reopened. `claude auth status` "
                         "cannot tell you this - it reports login and plan, and "
                         "says pro just as happily while every call is refused")
    args = ap.parse_args()

    if args.check:
        return 0 if window_is_open(args.model) else 1

    orph = orphans()
    if args.adopt:
        o = orph.get(args.adopt)
        if not o:
            print(f"no orphan runs found for stamp {args.adopt}", file=sys.stderr)
            return 2
        if len(o["tier"]) != 1:
            print(f"runs under {args.adopt} disagree on tier: {o['tier']}. "
                  f"Refusing to guess.", file=sys.stderr)
            return 2
        tier = o["tier"].pop()
        arms, tasks = sorted(o["arms"]), sorted(o["tasks"])
        man = {
            "stamp": args.adopt, "tier": tier, "arms": arms, "tasks": tasks,
            "runs": o["runs"], "model": args.model, "dry_run": False,
            "adopted": True,
            "note": ("reconstructed from run files by resume.py --adopt; this "
                     "sweep predates manifests. model was supplied by hand and "
                     "is not verifiable from the records"),
            "resume_cmd": (
                f"python benchmarks/harness.py --tier {tier} --runs {o['runs']}"
                + (f" --model {args.model}" if args.model else "")
                + f" --arms {','.join(arms)}"
                + f" --tasks {','.join(tasks)}"
                + f" --yes --resume {args.adopt}"),
        }
        (RUNS / f"{args.adopt}.manifest.json").write_text(
            json.dumps(man, indent=2), encoding="utf-8")
        print(f"adopted {args.adopt}: tier {tier}, {len(arms)} arms, "
              f"{len(tasks)} tasks, {o['runs']} run(s) per cell")
        print(f"  {o['done']} good, {o['errored']} errored on disk")
        if not args.model:
            print("  WARNING: no --model given. The resume line will use the "
                  "CLI default,\n  which may not be the model the earlier runs "
                  "used. Mixing models in one\n  table is exactly what the "
                  "Limitations section says not to do.")

    all_sweeps = sweeps()
    if not all_sweeps:
        print("no sweep manifests in benchmarks/runs/.")
        if orph:
            print("\nBut there are run files with no manifest - sweeps started "
                  "before manifests\nexisted. Adopt one and this tool can drive "
                  "it:\n")
            for stamp, o in sorted(orph.items()):
                tier = "/".join(sorted(o["tier"]))
                print(f"  {stamp}  tier {tier}  {o['done']} good, "
                      f"{o['errored']} errored")
                print(f"    python benchmarks/resume.py --adopt {stamp} "
                      f"--model <the model you used>")
        return 0

    if orph:
        print(f"({len(orph)} sweep(s) have run files but no manifest - "
              f"see --adopt)\n")

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
          "costs")
    print("only the runs that are actually missing.")
    print()
    print("Check the window has reopened FIRST. `claude auth status` cannot "
          "tell you:")
    print("it reports login and plan, and says subscriptionType: pro just as")
    print("happily while every single call is being refused. This spends one")
    print("trivial call and answers honestly:")
    print()
    print(f"  python benchmarks/resume.py --check "
          f"--model {target['model'] or 'haiku'}")
    print()

    if args.run:
        print(f"running: {target['resume_cmd']}\n")
        return subprocess.run(target["resume_cmd"].split(), cwd=REPO).returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
