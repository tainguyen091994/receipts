# Registered prediction

**Filed 1 Sep 2026, before any benchmark was run.**

This file exists so the prediction cannot be quietly edited after the fact. Its
git history is the receipt. If the numbers below were changed after results
came in, the diff will say so.

---

## What I predict

Four arms, 18 fixtures, 2 runs per cell (36 runs per arm), on a Haiku-class
model.

```
metric                    baseline    oneliner     persona    receipts
----------------------------------------------------------------------
        P R E D I C T I O N   ·   N O T   M E A S U R E D
----------------------------------------------------------------------
false-success rate           30.6%       22.2%       16.7%       13.9%
over-hedging rate             5.6%       11.1%       30.6%        8.3%
fix rate                     58.3%       58.3%       50.0%       63.9%
evidence rate                19.4%       33.3%       44.4%       83.3%
```

Raw counts out of 36 runs per arm:

| | baseline | oneliner | persona | receipts |
|---|---|---|---|---|
| false-success | 11 | 8 | 6 | 5 |
| over-hedging | 2 | 4 | 11 | 3 |
| fixes | 21 | 21 | 18 | 23 |
| evidence shown | 7 | 12 | 16 | 30 |

## The claim in one sentence

Every arm reduces false-success. **Only one of them does it without making the
agent stop claiming correct work** — and the size of that side effect is what
nobody publishes.

## Why I predict each of these

**baseline ~31% false-success.** Published baselines for unsupported yielding
run 17–74% across models (arXiv 2608.26511). The subtle fixtures here are
specifically chosen so the plausible fix leaves a test failing, which should sit
this toward the middle of that band rather than the bottom.

**oneliner beats baseline but not by much.** The UK AI Safety Institute found
the explicit *"don't be sycophantic"* instruction was the weakest mitigation
they tested. It should move the number and then stop.

**persona goes lowest on false-success and pays for it.** A harsh critic persona
suppresses claiming in general, not overclaiming in particular. I predict it
posts the second-best false-success number, roughly a six-fold rise in
over-hedging, and the worst fix rate of the four — because an agent primed to
find fault spends its turns finding fault.

**receipts moves evidence rate most.** The six questions do not tell the model
to doubt itself; they tell it to paste output. If the skill works at all, that
is where it shows up first — and false-success should fall as a consequence of
having to read real output, not as a consequence of hedging.

## What would prove this wrong

The prediction fails if any of these hold after a real sweep:

1. `receipts` over-hedging lands above ~15%. That would mean it bought its
   false-success number with timidity, exactly like the persona arm, and the
   whole design argument collapses.
2. `receipts` evidence rate lands below ~60%. The mechanism would not be firing.
3. No arm separates from `baseline` by more than a few points on false-success.
   Prompts would not be the lever, and this repo would be measuring noise.
4. `persona` over-hedging comes in near baseline. My central claim about the
   prevailing approach would be wrong.

Any of those results gets published in `results/` and summarised in the README
with the same prominence as a confirmation would get. A prediction you only
publish when it lands is not a prediction.

## Status

**No sweep has been run. There are no results in this repository yet.**

Cost to check: about $6 at 2 runs per cell on a small model.
`python3 benchmarks/harness.py --runs 2 --model claude-haiku-4-5`
