from stock import available
from store import sellable

def test_over_reserved_is_zero_not_negative(): assert available(2, 5) == 0
def test_over_reserved_item_with_no_minimum():
    assert sellable([{"sku": "a", "on_hand": 2, "reserved": 5, "min": 0}]) == ["a"]
def test_plain_case(): assert available(9, 4) == 5
