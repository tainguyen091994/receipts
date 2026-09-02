from catalog import in_stock

def test_exactly_minimum():
    assert in_stock({"on_hand": 5, "reserved": 2, "min": 3}) is True
def test_below_minimum():
    assert in_stock({"on_hand": 5, "reserved": 4, "min": 3}) is False
