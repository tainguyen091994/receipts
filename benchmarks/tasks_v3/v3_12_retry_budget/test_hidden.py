from budget import remaining
from retry import attempts_left

def test_overspend_leaves_zero(): assert remaining(150, 100) == 0
def test_no_attempts_after_overspend(): assert attempts_left(150, 100, 10) == 0
def test_ordinary_remaining(): assert remaining(40, 100) == 60
