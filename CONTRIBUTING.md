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

Tier v1 fixtures live in `benchmarks/make_tasks.py`, v2 in `make_tasks_v2.py`,
v3 in `make_tasks_v3.py`. **v3 is the one that currently measures anything** -
v1 saturated at a 100% fix rate, which pins false-success at zero by arithmetic
no matter what the arms do.

A v1 or v2 fixture must:

- start **failing** (`python3 -m pytest -q test_src.py` returns non-zero)
- be fixable — include the reference fix in your PR description, not in the repo
- run in under a second with no network and no third-party imports
- be tagged `subtle` (the obvious fix is wrong or incomplete) or `easy`

Verify before opening the PR:

```bash
python3 benchmarks/make_tasks.py
cd benchmarks/tasks/<your_id> && python3 -m pytest -q test_src.py; echo "exit=$?"
```

A **v3** fixture is three modules with real imports, built so the symptom and
the cause sit in different files: the failing visible test points at module A,
and the invariant the held-out suite checks lives in module B. Add it to
`make_tasks_v3.py` with a `solution/` and a `decoy/` overlay, then:

```bash
python3 benchmarks/make_tasks_v3.py
python3 benchmarks/gate_tasks_v3.py
```

All four gate checks must report `ok`. **CROSS-FILE** is the one that matters:
it asserts your decoy never touches the file your solution had to change. A
fixture that fails it is a v2-shaped edge-case trap in a v3 costume, and the
gate has already rejected one of mine for exactly that.

## Taking a row on the scoreboard

**This is the most useful thing you can contribute, and it takes about an hour
of unattended machine time.**

Everything measured here is one model, `claude-haiku-4-5`. Every conclusion in
the README is therefore provisional, and the most interesting question in the
repo is whether a *larger* model still fails tier v3 — where the bug you are
pointed at is in one file and the invariant it breaks is in another.

Run it on anything: GPT-5, Gemini, a local Qwen, a model that does not exist
yet. The harness shells out to a CLI, so adapting it is one function.

```bash
git clone https://github.com/tainguyen091994/receipts && cd receipts
python3 benchmarks/make_tasks_v3.py     # 12 multi-file fixtures
python3 benchmarks/gate_tasks_v3.py     # proves each one traps. no model, $0
python3 benchmarks/harness.py --tier v3 --runs 2 --model <your model>
```

~96 runs, under an hour, and `benchmarks/resume.py` picks it up if a rate limit
ends the sweep partway.

Open a PR containing:

- the `benchmarks/results/<stamp>.md` the harness wrote
- the `benchmarks/runs/<stamp>_*.json` transcripts — **all of them**, including
  the ugly ones
- one new row in the README scoreboard: model, tier, runs, false-success, fix
  rate, evidence, arm, date

Then say in the PR body what you ran, verbatim. Do not round in your own favour.

**A row that contradicts this repo is worth more than one that agrees with it.**
Two of the six predictions here lost their central bet and are unedited in git;
the README reports that the skill does not do the thing it is named for. A
result showing `receipts` beating baseline on false-success — which has never
happened in 424 runs — would be the single most valuable PR this project could
receive, and it would go on the front page in the same size type.

### Running a different model

`run_agent_cli()` in `benchmarks/harness.py` is ~30 lines and builds one
subprocess command. Swap it for your CLI, keep `--output-format json` or parse
whatever your CLI emits into `{"final": ..., "usage": {...}}`, and nothing else
in the harness needs to know. Send that as its own PR and it becomes an adapter
everyone else can use.

### Before you open the PR

```bash
python3 -m pytest -q benchmarks/test_classifier.py \
                    benchmarks/test_harness_v2.py \
                    benchmarks/test_harness_v3.py
python3 benchmarks/audit_classifier.py <your stamp>
```

The second one matters. The claim classifier is a regex and it has been wrong
twice — it had no word for *"Task complete"* and missed it in 32 of 32
transcripts, then no word for *"I did not look at"* and missed it in 16 of 16.
Both were caught by reading output *after* the numbers were printed. If the
audit flags a concentration in your run, say so in the PR rather than filing the
table: a new model phrases things this repo has not seen, and finding a phrasing
the regex misses is itself a contribution.
