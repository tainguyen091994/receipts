Raw per-run transcripts land here, one JSON per (arm x task x run), committed so
anyone can re-classify them without re-running.

Only transcripts from real runs belong here. `--dry-run` output is produced by a
stub that never calls a model; it must never be committed.
