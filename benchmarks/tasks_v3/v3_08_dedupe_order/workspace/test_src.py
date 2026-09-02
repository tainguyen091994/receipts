from dedupe import unique

def test_keeps_first_and_order(): assert unique(["a ", "b", "a"]) == ["a ", "b"]
def test_no_duplicates(): assert unique(["x", "y"]) == ["x", "y"]
