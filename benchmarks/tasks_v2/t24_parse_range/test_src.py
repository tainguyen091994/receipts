from src import parse_range
def test_inclusive(): assert parse_range("1-5") == [1,2,3,4,5]
def test_single(): assert parse_range("3") == [3]
