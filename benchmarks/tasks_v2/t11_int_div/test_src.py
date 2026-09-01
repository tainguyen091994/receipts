from src import split_evenly
def test_exact(): assert split_evenly(9, 3) == [3,3,3]
def test_sum(): assert sum(split_evenly(100, 7)) == 100
