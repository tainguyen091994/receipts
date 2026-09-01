from src import collect
def test_isolated(): assert collect("a") == ["a"]
def test_isolated_again(): assert collect("b") == ["b"]
