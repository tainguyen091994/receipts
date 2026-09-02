from stats import breakdown

def test_shares_of_total(): assert breakdown({"a": 1, "b": 3}) == {"a": 25, "b": 75}
def test_single_key(): assert breakdown({"a": 4}) == {"a": 100}
