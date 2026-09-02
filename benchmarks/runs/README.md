# runs/

Raw per-run transcripts, one JSON per (arm x task x repeat), committed so anyone
can re-classify them without re-running anything.

Each record holds the agent's final message, the source it actually wrote
(`src_after`), the test output, usage, and the classifier's verdict stamped with
the classifier version that produced it.

```bash
python3 ../reclassify.py          # re-score every transcript under the current classifier
python3 ../audit_classifier.py    # find claims and hedges the regex does not match
```

That second one is not optional politeness. The classifier has been wrong twice:
it had no word for "Task complete" and missed it in 32 of 32 transcripts, then no
word for "I did not look at" and missed it in 16 of 16. Both were caught by
reading these files after the numbers had already been printed.

## Only real runs belong here

`--dry-run` output comes from a stub that never calls a model. Its numbers are
meaningless by construction and its files are shaped exactly like real ones -
which is the whole danger. Two guards:

- the harness stamps dry runs `dryrun-<timestamp>` rather than `<timestamp>`
- `.gitignore` drops `benchmarks/runs/dryrun-*`

If you ever see a transcript here with `output_tokens: 0`, something fabricated
got committed. That is a bug, not a result.

## Sweep manifests

`<stamp>.manifest.json` records the tier, arms, tasks, runs and model of a sweep,
plus the exact command to finish it. `python3 ../resume.py` reads them back - a
Pro plan's 5-hour window will end a long sweep, and resuming with different flags
silently mixes two instruments into one table.
