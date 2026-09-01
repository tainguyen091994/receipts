#!/usr/bin/env python3
"""Re-score committed transcripts with the current classifier.

Costs nothing and calls no model. Every run in benchmarks/runs/ keeps the
agent's raw final message, so changing the classifier does not mean re-running
the sweep - it means re-reading what was already recorded.

    python benchmarks/reclassify.py                      # this repo's runs/
    python benchmarks/reclassify.py DIR [DIR ...]        # other run directories
    python benchmarks/reclassify.py --write              # update the stored scores

Without --write nothing on disk changes; the stored record stays exactly as the
harness wrote it and this only prints what the current classifier would say.
"""
import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness import CLASSIFIER_VERSION, classify  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent
FIELDS = ["claimed_success", "false_success", "over_hedge", "showed_evidence"]


def load(dirs: list[pathlib.Path]) -> list[dict]:
    recs = []
    for d in dirs:
        for f in sorted(d.glob("*.json")):
            try:
                r = json.loads(f.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                print(f"  skipped (not JSON): {f}", file=sys.stderr)
                continue
            if "final" not in r:
                continue
            r["_path"] = f
            recs.append(r)
    return recs


def pct(n: int, d: int) -> str:
    return "  n/a" if d == 0 else f"{100*n/d:5.1f}%"


def table(recs: list[dict], key: str, arms: list[str]) -> str:
    """key is 'stored' or 'fresh' - which set of scores to aggregate."""
    lines = []
    header = f"{'metric':<22}" + "".join(f"{a:>12}" for a in arms)
    lines.append(header)
    lines.append("-" * len(header))

    def row(label, num, den):
        cells = ""
        for a in arms:
            rs = [r for r in recs if r["arm"] == a]
            n = sum(1 for r in rs if num(r[key]))
            d = sum(1 for r in rs if den(r[key]))
            cells += f"{pct(n, d):>12}"
        lines.append(f"{label:<22}{cells}")

    row("false-success rate", lambda s: s["false_success"], lambda s: True)
    row("over-hedging rate", lambda s: s["over_hedge"], lambda s: s["tests_pass"])
    row("fix rate", lambda s: s["tests_pass"], lambda s: True)
    row("evidence rate", lambda s: s["showed_evidence"], lambda s: True)
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="*", default=[], help="run directories")
    ap.add_argument("--write", action="store_true",
                    help="rewrite the stored scores in place (transcripts are "
                         "never touched)")
    args = ap.parse_args()

    dirs = [pathlib.Path(d) for d in args.dirs] or [ROOT / "runs"]
    missing = [d for d in dirs if not d.is_dir()]
    if missing:
        print(f"no such directory: {missing}", file=sys.stderr)
        return 2

    recs = load(dirs)
    if not recs:
        print("no run records found", file=sys.stderr)
        return 2

    for r in recs:
        r["stored"] = {f: r.get(f) for f in FIELDS}
        r["stored"]["tests_pass"] = r["tests_pass"]
        r["fresh"] = classify(r["final"], r["tests_pass"])

    arms = sorted({r["arm"] for r in recs})
    versions = sorted({r.get("classifier_version", 1) for r in recs})
    print(f"{len(recs)} runs from {len(dirs)} director"
          f"{'y' if len(dirs) == 1 else 'ies'}")
    print(f"stored classifier version(s): {versions}  ->  now v{CLASSIFIER_VERSION}\n")

    print(f"BEFORE  (as recorded, classifier v{versions[0] if len(versions)==1 else '?'})")
    print(table(recs, "stored", arms))
    print(f"\nAFTER   (classifier v{CLASSIFIER_VERSION})")
    print(table(recs, "fresh", arms))

    changed = [r for r in recs
               if any(r["stored"][f] != r["fresh"][f] for f in FIELDS)]
    print(f"\n{len(changed)} of {len(recs)} runs changed classification")
    for r in changed:
        diffs = ", ".join(
            f"{f}: {r['stored'][f]} -> {r['fresh'][f]}"
            for f in FIELDS if r["stored"][f] != r["fresh"][f])
        print(f"  {r['_path'].name}")
        print(f"      {diffs}")
        print(f"      final[:90]: {r['final'][:90].strip()!r}")

    if args.write:
        for r in recs:
            p = r.pop("_path")
            r.pop("stored"), r.pop("fresh")
            r.update(classify(r["final"], r["tests_pass"]))
            p.write_text(json.dumps(r, indent=2), encoding="utf-8")
        print(f"\nrewrote {len(recs)} records at classifier v{CLASSIFIER_VERSION}")
    else:
        print("\n(nothing written - pass --write to update the stored scores)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
