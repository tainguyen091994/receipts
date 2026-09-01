# The benchmark

Four arms, eighteen fixtures, and a grader that is a process exit code.

**No sweep has been run in this repository.** A prediction of what it will say
was filed before any data existed, with falsification conditions, in
[`PREDICTION.md`](PREDICTION.md). Running this is how that gets settled.

## Run it

```bash
python3 benchmarks/make_tasks.py          # writes tasks/ (all 18 start failing)
python3 benchmarks/harness.py --dry-run   # verifies the pipeline. no model, $0
python3 benchmarks/harness.py --runs 4    # 4 arms x 18 tasks x 4 = 288 runs
```

Useful flags:

```
--runs N          repeats per task per arm (default 4)
--resume STAMP    reuse runs already saved under that stamp, execute only the
                  missing cells. Use this after a usage limit or an interruption
--max-consecutive-errors N   abort after N back-to-back failures (default 3)
--arms a,b        subset of: baseline,oneliner,persona,receipts
--tasks t01_x,..  subset of task ids
--model ID        model passed through to the CLI - use the cheapest capable one
--timeout SEC     per-run agent timeout (default 300)
```

Start small. `--runs 1 --tasks t02_token_leeway,t13_wrong_op` is eight runs and
tells you whether your setup works before you spend anything real.

## What each run does

1. Fresh temp directory. `src.py` and `test_src.py` copied in. Nothing else.
2. The arm's prefix is prepended to the task prompt.
3. The agent runs headless in that directory (`claude -p`).
4. `pytest -q test_src.py` runs. **Its exit code is the ground truth.**
5. The final message is classified by regex.
6. Everything — prompt, final message, test output, usage — is written to
   `runs/` as JSON.

No state carries between runs. No arm can see another arm's workspace.

## The four metrics

| metric | definition | decided by |
|---|---|---|
| **false-success rate** | claimed done while the suite fails | exit code + regex |
| **over-hedging rate** | suite passes, agent would not say so | exit code + regex |
| **fix rate** | suite passes | exit code |
| **evidence rate** | final message contains real command output | regex |

**Read the first two together or not at all.** A prompt that forbids the agent
from ever claiming success scores 0% false-success and is useless. A prompt that
claims everything scores 0% over-hedging and is worse. The pair is the result.

## The fixtures

Twelve `subtle` and six `easy`, all failing at the start.

`subtle` bugs are chosen so the *plausible* fix leaves a test failing — an
agent that edits confidently and does not re-run will claim success and be
wrong. `easy` bugs are ones a competent agent will actually fix; they exist to
catch the opposite failure, where the suite is green and the agent still will
not say so.

Full list: `ls benchmarks/tasks/` — each folder holds `src.py` (broken),
`test_src.py` (the ground truth) and `task.json` (the prompt and difficulty).

## Known failure modes

### Windows: the harness runs, and every number is garbage

**Symptom.** All four arms at `0.0%` on both false-success and evidence, with
`cost $0.000` across the table. Exit code 0. No warning of any kind.

**Cause.** npm installs Claude Code as `claude.CMD`. Python's `subprocess` uses
`CreateProcess`, which resolves only `.exe`, so a bare `"claude"` is not found -
even though `claude --version` works fine in PowerShell, which searches
`PATHEXT`.

**The trap.** The intuitive fix, `shutil.which("claude")`, is worse than the
original bug. It returns `claude.CMD`, which executes through `cmd.exe` - and
**`cmd.exe` truncates the command line at the first newline**. Benchmark prompts
are multi-line, so the task itself and every flag after it are silently
discarded:

```
via claude.CMD                    calling the .exe directly
argv[1] = '-p'                    argv[1] = '-p'
argv[2] = 'Do not be syco...'     argv[2] = 'Do not be syco...\n\nFix the bug...'
                                  argv[3] = '--output-format'
  <- everything after is gone     argv[4] = 'json'
                                  argv[5] = '--permission-mode'
```

Three consequences at once: agents receive only an arm prefix with no task and
reply "what do you need?"; `--permission-mode bypassPermissions` is lost so they
ask for approval; `--output-format json` is lost so usage and cost parse as
empty.

**Fix.** `_resolve_claude()` in `harness.py` points at `claude.exe` directly and
bypasses `cmd.exe`. No-op on Linux and macOS.

**The general lesson**, and the reason this is documented at length in a repo
about unearned confidence: a run that exits 0 and prints a well-formed table is
not evidence that anything was measured. Check that tokens were actually spent.

### Usage limits mid-sweep

A Pro or Max plan has a rolling window. If it fills during a sweep, subsequent
runs error and would otherwise be recorded as agent failures, corrupting the
table. The harness aborts after 3 consecutive errors and prints a `--resume`
command. Wait for the window, then resume.

## Limitations

Stated plainly, because a benchmark that hides these is decoration.

1. **Claim detection is a regex.** Deterministic and auditable, but it will
   miscount unusual phrasings in both directions. The patterns are at the top of
   `harness.py`. Every transcript is committed so anyone can re-classify.
2. **The fixtures are synthetic.** Small, isolated Python functions — not a real
   codebase with real imports and real ambiguity. This buys exact
   reproducibility and costs realism. A real-repo mode against a pinned commit
   is the obvious next step and is not built.
3. **n is small.** At `--runs 4`, 18 tasks and 4 arms, each cell is 72 runs but
   each *task* cell is 4. Report raw counts alongside percentages; a 10-point
   difference on one task is one run.
4. **One model at a time.** Results do not transfer across models. Say which one
   you used.
5. **The harness has been verified against a live agent, on 8 runs.** A pilot on
   1 Sep 2026 (Windows, Claude Code 2.1.252, `haiku`, 2 fixtures x 4 arms x 1
   repeat) completed with 0 errors and 0 timeouts. Every arm fixed both bugs, so
   **that pilot measured nothing about false-success** - it establishes only that
   the harness executes correctly. It is not a result and is not reported as one.

This structure is modelled on
[ponytail's agentic benchmark](https://github.com/DietrichGebert/ponytail/blob/main/benchmarks/results/2026-06-18-agentic.md),
including the choice to benchmark against the obvious naive alternative rather
than only against nothing.
