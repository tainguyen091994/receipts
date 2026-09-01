from cart import cart_total
from pricing import line_total

def test_discount_applies_to_the_line():
    # 333 cents x 3 units, 10% off = 899.1 -> 899
    assert line_total(333, 3, 10) == 899
def test_cart_sums_lines():
    assert cart_total([(100, 2), (250, 1)]) == 450
