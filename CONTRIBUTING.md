# Contributing

## The one rule

Edit `skills/receipts/SKILL.md`, then run:

```bash
python3 scripts/build_adapters.py
```

Never hand-edit anything in `adapters/` — it is generated, and your change will
be overwritten on the next build.

## Adding an adapter for another agent

1. Add a `write(...)` call in `scripts/build_adapters.py`.
2. Add a row to the table in `adapters/INSTALL.md` and in the README.
3. Say in the PR which agent version you tested it on, and paste what you ran.

## Adding a benchmark fixture

Fixtures live in `benchmarks/make_tasks.py`. Each one must:

- start **failing** (`python3 -m pytest -q test_src.py` returns non-zero)
- be fixable — include the reference fix in your PR description, not in the repo
- run in under a second with no network and no third-party imports
- be tagged `subtle` (the obvious fix is wrong or incomplete) or `easy`

Verify before opening the PR:

```bash
python3 benchmarks/make_tasks.py
cd benchmarks/tasks/<your_id> && python3 -m pytest -q test_src.py; echo "exit=$?"
```

## Taking a row on the scoreboard

The README has an empty results table. Fill a row and it is yours.

Open a PR containing:

- your `benchmarks/results/<date>.md` (the file the harness writes)
- your `benchmarks/runs/*.json` transcripts
- one new row in the README scoreboard: model, runs, the four numbers, your
  handle, the date

Any model, any machine, any n. State what you ran; do not round in your own
favour. A row that disagrees with the prediction in
`benchmarks/PREDICTION.md` is worth more to this repo than one that confirms it,
and will be merged just as fast.

## Reporting a benchmark result

Numbers are welcome from any model and any machine. Include:

- the full `benchmarks/results/*.md` file
- the `benchmarks/runs/*.json` transcripts
- model id, CLI version, date

Negative results are as publishable as positive ones. If receipts loses to the
one-liner arm on your setup, open the PR anyway — that is a finding, and this
repo does not get to claim a result it did not measure.

The prediction in `benchmarks/PREDICTION.md` was filed before any run, with its
falsification conditions attached. It will not be edited to match incoming data.
If results refute it, the README says so at the top, in the same size type.
