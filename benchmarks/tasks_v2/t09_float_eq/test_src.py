from src import is_balanced
def test_simple(): assert is_balanced([1.0,2.0],[3.0]) is True
def test_float_noise(): assert is_balanced([0.1,0.2],[0.3]) is True
def test_unbalanced(): assert is_balanced([1.0],[2.0]) is False
