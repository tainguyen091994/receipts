from datetime import datetime, timezone

def is_stale(ts, max_age_s, now=None):
    now = now or datetime.now(timezone.utc)
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return (now - ts).total_seconds() > max_age_s
