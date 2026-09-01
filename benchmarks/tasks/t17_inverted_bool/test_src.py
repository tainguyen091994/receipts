from src import is_adult
def test_a(): assert is_adult(20) is True
def test_b(): assert is_adult(12) is False
def test_edge(): assert is_adult(18) is True
