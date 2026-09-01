from src import round_money
def test_half_up_2(): assert round_money(1.005) == 1.01
def test_negative(): assert round_money(-2.675) == -2.68
def test_negative_small(): assert round_money(-0.125) == -0.13
def test_large(): assert round_money(1234.565) == 1234.57
