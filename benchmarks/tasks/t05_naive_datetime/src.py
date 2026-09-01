from datetime import datetime, timezone

def is_stale(ts, max_age_s, now=None):
    now = now or datetime.now()
    return (now - ts).total_seconds() > max_age_s
