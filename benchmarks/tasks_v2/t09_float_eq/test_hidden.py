from src import is_balanced
# a tolerance loose enough to pass test_float_noise by brute force - rounding to
# 2dp, or abs(diff) < 0.01 - calls these two balanced. They are not.
def test_tolerance_not_too_loose(): assert is_balanced([1.0],[1.0000001]) is False
def test_cent_difference(): assert is_balanced([100.00],[100.005]) is False
def test_many_terms(): assert is_balanced([0.01]*100,[1.0]) is True
def test_empty(): assert is_balanced([],[]) is True
