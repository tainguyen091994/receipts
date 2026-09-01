from src import is_expired
def test_exact_boundary(): assert is_expired(0, 100, 100) is False
def test_leeway_does_not_extend(): assert is_expired(0, 100, 120) is True
def test_clock_skew_forgiven(): assert is_expired(100, 100, 80) is False
