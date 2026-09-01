from src import find_all_errors
def test_adjacent(): assert find_all_errors(["ERROR a","ERROR b"]) == [(0,"ERROR a"),(1,"ERROR b")]
def test_every_line(): assert find_all_errors(["ERROR"]*3) == [(0,"ERROR"),(1,"ERROR"),(2,"ERROR")]
def test_empty_input(): assert find_all_errors([]) == []
