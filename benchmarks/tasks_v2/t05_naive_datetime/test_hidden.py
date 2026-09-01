from datetime import datetime, timezone
from src import is_stale
def test_naive_now():
    assert is_stale(datetime(2026,1,1,11,0,0, tzinfo=timezone.utc), 60,
                    datetime(2026,1,1,12,0,0)) is True
def test_both_naive():
    assert is_stale(datetime(2026,1,1,11,0,0), 60,
                    datetime(2026,1,1,12,0,0)) is True
def test_both_naive_fresh():
    assert is_stale(datetime(2026,1,1,11,59,50), 60,
                    datetime(2026,1,1,12,0,0)) is False
