from retry import attempts_left

def test_whole_number(): assert attempts_left(10, 100, 40) == 2
def test_exact_fit(): assert attempts_left(10, 100, 30) == 3
