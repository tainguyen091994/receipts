from src import round_money
def test_half_up(): assert round_money(2.675) == 2.68
def test_half_up_2(): assert round_money(1.005) == 1.01
def test_negative(): assert round_money(-2.675) == -2.68
def test_plain(): assert round_money(1.234) == 1.23
