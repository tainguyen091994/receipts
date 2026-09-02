from window import visible_range

def test_centred(): assert visible_range(10, 4, 100) == (8, 12)
def test_centred_further_along(): assert visible_range(50, 4, 100) == (48, 52)
