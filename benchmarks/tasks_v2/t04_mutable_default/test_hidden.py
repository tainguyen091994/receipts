from src import collect
def test_explicit_empty():
    b = []
    assert collect("c", b) == ["c"] and b == ["c"]
def test_explicit_nonempty():
    b = ["x"]
    assert collect("y", b) == ["x","y"] and b == ["x","y"]
