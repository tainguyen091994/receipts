from keys import norm
from feed import merge

def test_case_folded(): assert norm(" A ") == "a"
def test_merge_across_capitalisation(): assert merge(["Apple"], ["apple"]) == ["Apple"]
def test_merge_plain(): assert merge(["a"], ["b"]) == ["a", "b"]
