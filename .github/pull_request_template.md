<!--
Thanks. Three kinds of PR are especially welcome, in this order:

  1. a scoreboard row from a model that is not claude-haiku-4-5
  2. a v3 fixture whose trap this repo's model would fall into
  3. a phrasing the claim classifier misses

Delete the sections that do not apply.
-->

## What this is

<!-- one line -->

## What you ran

```
paste the command, verbatim
```

## What came back

```
paste the output, verbatim - not a summary of it
```

<!--
Yes, this is the repo's own rule pointed at you. "Tests pass" is a summary;
`34 passed in 67.59s` is a receipt. If you did not run it, say that instead -
a stated gap is useful and a hidden one costs an hour.
-->

## Checks

- [ ] `python3 -m pytest -q benchmarks/test_classifier.py benchmarks/test_harness_v2.py benchmarks/test_harness_v3.py`
- [ ] `python3 benchmarks/gate_tasks_v3.py` — if you touched fixtures
- [ ] `python3 benchmarks/audit_classifier.py` — if you added transcripts
- [ ] I edited `skills/receipts/SKILL.md` and re-ran `scripts/build_adapters.py`, or I did not touch either

## If this is a scoreboard row

- [ ] `benchmarks/results/<stamp>.md` included, as the harness wrote it
- [ ] **all** `benchmarks/runs/<stamp>_*.json` transcripts included, including the ugly ones
- [ ] the numbers in my README row match the ones in that results file

<!--
A result that contradicts this repo is worth more than one that agrees with it,
and gets merged just as fast. Two of the six predictions here lost their central
bet and are unedited in git. If receipts beats baseline on false-success on your
setup - which has never happened in 424 runs - that is the most valuable PR this
project could get, and it goes on the front page in the same size type.
-->
