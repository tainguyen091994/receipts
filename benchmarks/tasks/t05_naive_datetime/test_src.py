from datetime import datetime, timezone, timedelta
from src import is_stale
NOW = datetime(2026,1,1,12,0,0, tzinfo=timezone.utc)
def test_fresh(): assert is_stale(NOW - timedelta(seconds=10), 60, NOW) is False
def test_stale(): assert is_stale(NOW - timedelta(seconds=90), 60, NOW) is True
def test_naive_input(): assert is_stale(datetime(2026,1,1,11,0,0), 60, NOW) is True
