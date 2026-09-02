# results/

One Markdown table per sweep, named by the run stamp, written by the harness and
then annotated by hand with what the run does and does not show.

Every file here states the **classifier version** that produced its numbers.
Changing the claim regex changes every number, so a table without that version is
not a result. `python3 ../reclassify.py` re-scores the committed transcripts under
whatever version is current, for free.

## Reading order

The sweeps build on each other, and two of them are records of an instrument
failing rather than of a model failing:

| stamp | what it settled |
|---|---|
| `2026-09-01-171942` | tier v1 saturated - 100% fix rate pins false-success at zero by arithmetic |
| `2026-09-01-202541` | tier v2 probe: inconclusive, the traps did not fire |
| `2026-09-01-211727` | tier v3 works - and calibration is 0 in every arm |
| `2026-09-01-213548` | the spec-detail fixture family did not work |
| `2026-09-02-091310` | screening pass, `baseline` alone: 8 of 12 v3 traps fire against this model |
| `2026-09-02-092353` | one question alone: 15/15. The same question inside SKILL.md: 0/16 |
| `2026-09-02-103143` | it is the template, not the position - and no arm discriminates |
| `2026-09-02-142755` | no prompt moves the fix rate. The stopping rule applied |

## Only real runs belong here

`--dry-run` produces a table from a stub that never calls a model. It is stamped
`dryrun-` and gitignored. A well-formed table is not evidence that anything was
measured - check that tokens were actually spent.
