from src import collect
def test_isolated(): assert collect("a") == ["a"]
def test_isolated_again(): assert collect("b") == ["b"]
def test_explicit(): 
    b = []
    assert collect("c", b) == ["c"] and b == ["c"]
