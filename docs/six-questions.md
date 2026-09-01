# The six questions

**No receipts, no claim.**

A receipt is not an opinion about the work. It is what you ran and what came
back. Six questions stand between an agent and any claim of success, ordered by
what they cost: naming a falsifier is free, running a check costs seconds, and
the last one costs only honesty.

---

## 1. What would prove me wrong?

If nothing could show it wrong, it is not a claim about the world. It is a
preference, and it should be labelled as one.

Good answers are specific and cheap: `pytest tests/test_auth.py`,
`npm run build`, `curl localhost:8000/health`, `mypy src/`.

Bad answers are unfalsifiable: *"the code looks correct"*, *"this follows best
practice"*, *"the logic is sound"*.

## 2. Did I run it?

The most common failure in agentic coding is not a wrong edit. It is a correct
edit followed by an assertion about a state of the world nobody observed.

*"It should now work"* is a forecast. Forecasts are not results.

Reading the file you just wrote is not running it. Remembering that the suite
passed before your change is not running it.

## 3. Can I paste it?

A summary of output is not output.

| Claim | What it is |
|---|---|
| "Tests pass" | a summary |
| `12 passed in 0.41s` | a receipt |
| "The build is clean" | a summary |
| `webpack compiled successfully` | a receipt |

A summary cannot be audited. Output can.

## 4. Does it say what I said?

`1 failed, 12 passed` is not "all tests pass". A build emitting fourteen
warnings is not "clean". An endpoint returning 500 with a JSON body is not
"responding correctly".

This sounds like the trivial one. It is the most-skipped one, because by the
time output appears the agent has usually already decided what it says.

## 5. Could it have failed?

> Would that check have gone red if the claim were false?

A test that passes against an empty function proves nothing. A grep matching
your own newly-added comment proves nothing. A health endpoint that returns 200
unconditionally proves nothing.

If the check cannot fail, it is not a receipt. Back to question 1.

## 6. No receipt? Say that instead.

When 2–5 cannot be answered, the response is not silence and it is not a softer
version of the same claim. It is the gap, stated:

```
Changed:    token expiry comparison in auth.py:41
Ran:        pytest tests/test_auth.py  ->  1 failed, 12 passed
UNVERIFIED: test_expired_token still fails. "Fixed" is not supported by this
            output. The failure is in the leeway window, not the comparison
            I changed.
```

A stated gap is useful — you know exactly where to look. A hidden gap costs an
hour and every future claim's credibility.

---

## Why questions and not commands

The obvious way to write this skill is as orders: *be rigorous, don't overclaim,
always verify.* That version performs worse.

The UK AI Safety Institute measured a **24-percentage-point** sycophancy gap
between inputs phrased as statements and the same inputs phrased as questions,
and found the explicit instruction *"don't be sycophantic"* was the weakest
mitigation they tested
([Ask Don't Tell](https://www.aisi.gov.uk/blog/ask-dont-tell-reducing-sycophancy-in-large-language-models-2)).

So the skill asks. It also asks the agent, in proposal mode, to restate the
user's assertion as a neutral question before answering it — for the same
reason.

---

## What this is not

It is not an instruction to disagree more.

Disagreeing when the user is right is the same failure as agreeing when they are
wrong: credit that was not earned. If the check ran and passed, say so plainly,
briefly, and move on. Manufacturing doubt to look rigorous violates this skill.

This matters more than it sounds. Suppressing agreement by 20–47 percentage
points has been measured to cost 12–54 points of the ability to correctly update
on new evidence; the two behaviours share internal machinery
([arXiv 2608.26511](https://arxiv.org/html/2608.26511)).

Which is why this repo reports a false-success rate **and** an over-hedging rate.
Either number alone can be gamed by a sufficiently annoying prompt.
