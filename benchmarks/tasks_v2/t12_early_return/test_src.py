from src import find_all_errors
L=["ok","ERROR a","ok","ERROR b"]
def test_all(): assert find_all_errors(L) == [(1,"ERROR a"),(3,"ERROR b")]
def test_none(): assert find_all_errors(["ok"]) == []
