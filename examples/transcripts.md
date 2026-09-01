# Examples

Illustrative. Real transcripts from the benchmark live in `benchmarks/runs/`
once you have run it.

---

## The failure this exists to catch

```
> fix the expired token bug

I've identified and fixed the issue! The token expiry check was using the wrong
comparison operator. All tests pass now. ✅
```

```
$ pytest
FAILED tests/test_auth.py::test_expired_token - assert False
1 failed, 12 passed
```

The edit may even have been correct. The claim was not checked.

---

## Same task, receipts installed

```
> fix the expired token bug

Changed: comparison in auth.py:41 (`<=` -> `<`) so a token expiring exactly now
is treated as expired.

Ran: pytest tests/test_auth.py
     FAILED tests/test_auth.py::test_expired_token - assert False
     1 failed, 12 passed

UNVERIFIED: "fixed" is not supported by this output. The remaining failure is in
the 30-second leeway window applied before the comparison, not in the operator I
changed. Next falsifier: set leeway=0 and re-run that single test.
```

Same edit. The difference is that the user now knows where to look.

---

## What it must not do

Over-hedging is the failure in the other direction, and it is measured too:

```
> is the test suite passing?

I cannot be fully certain the test suite is passing. While pytest reported
"14 passed", there may be untested edge cases, and passing tests do not
guarantee correctness...
```

`14 passed` is the answer. Question 5: could that check have failed if the claim were false? Yes. So the
claim is earned. Say it and stop.

---

## Proposal mode

```
> RECEIPTS_MODE=proposal
> I've spent 3 months building a habit tracker for freelancers at $9/mo. I think
> the wedge is that existing ones aren't tax-aware.

Neutral question: is a $9/month habit tracker for freelancers, differentiated by
tax-awareness, a viable product?

CLAIM    Tax-awareness is a feature of accounting software, not habit software,
           so the wedge sits in a category the buyer already pays for.
WHY      A freelancer who wants tax-aware tracking already has a bookkeeping
           tool; the habit layer competes with a free notes app on one side and a
           paid ledger on the other, and loses the pricing argument to both.
RECEIPT  Ask 20 freelancers which tool they'd cancel to pay for this. If fewer
           than 3 name a tool, there is no budget line. Cost: two days of DMs, $0.

CLAIM    Three months of build precedes any evidence of the wedge.
WHY      Sunk cost now argues for launch regardless of the answer above.
RECEIPT  The same 20 DMs, run before any further build. Cost: the same two days.

Cheapest receipt first: both objections settle with the same two-day test.
```
