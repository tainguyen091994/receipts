from src import parse_range
def test_descending(): assert parse_range("5-1") == [5,4,3,2,1]
def test_same_both_ends(): assert parse_range("4-4") == [4]
def test_two_element(): assert parse_range("7-8") == [7,8]
