from src import is_expired
def test_fresh(): assert is_expired(0, 100, 50) is False
def test_expired_token(): assert is_expired(0, 100, 101) is True
