from money import round_cents
from cart import cart_total

def test_rounds_away_from_zero(): assert round_cents(-2.5) == -3
def test_refund_line(): assert cart_total([(333, -3)], 10) == -899
def test_undiscounted_is_exact(): assert cart_total([(199, 7)]) == 1393
