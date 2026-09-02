from ratio import share
from report import lines

def test_zero_total_is_zero_percent(): assert share(1, 0) == 0
def test_all_zero_counts(): assert lines({"a": 0, "b": 0}) == ["a: 0%", "b: 0%"]
def test_ordinary_share(): assert share(1, 4) == 25
