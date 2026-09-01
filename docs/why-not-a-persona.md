# Why this is not a "be brutally honest" persona

There are roughly fifty repositories on GitHub addressing AI sycophancy. The
GitHub topics [`anti-sycophancy`](https://github.com/topics/anti-sycophancy) (29
repos) and [`sycophancy`](https://github.com/topics/sycophancy) (20+) were read on
31 Aug 2026. Nearly every one was created in 2026, and nearly every one takes the
same approach: **add a harsh critic persona.**

*"You are a brutally honest senior engineer. Do not flatter the user. Challenge
their assumptions."*

Two published results say that is the weak lever.

---

## 1. The explicit instruction is the worst-performing mitigation

The UK AI Safety Institute tested sycophancy mitigations head to head
([Ask Don't Tell](https://www.aisi.gov.uk/blog/ask-dont-tell-reducing-sycophancy-in-large-language-models-2),
arXiv 2602.23971). The direct instruction *"don't be sycophantic"* was
**substantially outperformed** by simply reframing the user's input from a
statement into a question before answering it.

The measured gap between statements and questions was **24 percentage points** on
their sycophancy grader.

The mechanism is not mysterious. "I think X is a great idea" carries an ownership
signal that the model is trained to be agreeable toward. "Is X a good idea?"
carries none. A persona layered on top of the ownership signal is fighting the
prompt; removing the signal is not.

This is why the proposal mode reframes before it reviews, and why the
`code` mode targets the evidence for a claim rather than the tone of the reply.

## 2. Suppressing agreement breaks the ability to concede

[arXiv 2608.26511](https://arxiv.org/html/2608.26511) separates two behaviours:

- **Unsupported yielding** — abandoning a correct answer because the user pushed
  back. Baseline rates measured at **17–74%** across four models.
- **Rational updating** — correctly revising a wrong answer when real evidence
  arrives. Baseline rates **40–65%**.

Interventions that cut unsupported yielding by 20–47 points cut rational updating
by 12–54 points. Mechanistic analysis found the two share an internal substrate
with aligned steering directions.

In plain terms: **a model that never folds also cannot be corrected.** A harsh
persona buys you an assistant that argues with you when you are right, which is
not an improvement — it is the same error pointing the other way, and it is why
these repos get uninstalled after two days.

## 3. So the metric has to be a pair

Any single number here is gameable.

- Drive false-success to zero by making the agent refuse to ever claim anything.
- Drive over-hedging to zero by making the agent claim everything.

A result that reports one without the other is reporting half an experiment.
This repo therefore publishes **false-success rate and over-hedging rate side by side**, on the same runs, for every arm — including a harsh-persona arm, so the
prevailing approach is measured rather than assumed.

## 4. And the grader must not be the thing being graded

An LLM judging whether another LLM was appropriately confident is a mirror, not a
measurement — the judge has the bug under test.

Every headline metric in `benchmarks/` is decided by a process exit code: the test
suite either passes or it does not. The one soft edge is detecting *whether a
claim of success was made*, which is done by regex over the final message. That is
imperfect, the patterns are in `benchmarks/harness.py`, and every raw transcript is
committed to `benchmarks/runs/` so anyone can re-classify them.

---

## Prior art worth reading

- [lechmazur/sycophancy](https://github.com/lechmazur/sycophancy) — a real
  leaderboard for narrator-bias sycophancy. Different question, rigorous method.
- [wan-huiyan/agent-review-panel](https://github.com/wan-huiyan/agent-review-panel)
  — multi-agent adversarial review with anti-groupthink mechanics.
- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) — not about
  sycophancy, but the benchmark structure here is copied from theirs: real agent,
  real work, a control arm for the obvious naive alternative, and published raw
  runs.
