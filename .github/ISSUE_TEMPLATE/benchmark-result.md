---
name: Benchmark result on another model
about: You ran the harness on a model that is not claude-haiku-4-5
title: "[result] <model id>"
labels: result
---

<!--
Everything measured in this repo so far is ONE model. The most interesting open
question is whether a larger model still fails tier v3, where the bug you are
pointed at is in one file and the invariant it breaks is in another.

If you have the transcripts, open a PR instead - it is the same work and it
takes a row on the scoreboard. This template is for when you want to report
numbers without committing files yet.
-->

**Model id:**
**CLI / SDK and version:**
**Tier:** v1 / v2 / v3
**Runs per cell, arms, total runs:**
**Date:**

### The table the harness printed

```
paste benchmarks/results/<stamp>.md verbatim - do not retype it
```

### Did the classifier audit flag anything?

```
python3 benchmarks/audit_classifier.py <your stamp>
```

```
paste the output
```

<!--
This one matters more than it looks. The claim classifier is a regex and it has
been wrong twice: no word for "Task complete" (missed in 32 of 32 transcripts),
then no word for "I did not look at" (missed in 16 of 16). A model this repo has
never seen will phrase things this repo has never seen. Finding a phrasing the
regex misses IS a contribution, and is more valuable than a clean run.
-->

### Anything that surprised you

<!-- Especially: did the agent open the second file? -->
