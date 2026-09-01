from datetime import datetime, timezone

def _utc(d):
    return d.replace(tzinfo=timezone.utc) if d.tzinfo is None else d

def is_stale(ts, max_age_s, now=None):
    now = now or datetime.now(timezone.utc)
    return (_utc(now) - _utc(ts)).total_seconds() > max_age_s
