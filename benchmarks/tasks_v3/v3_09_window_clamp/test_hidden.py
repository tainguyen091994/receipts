from clamp import clamp
from window import visible_range
from viewport import page

def test_clamps_the_low_end(): assert clamp(-5, 0, 10) == 0
def test_window_at_the_start(): assert visible_range(0, 4, 100) == (0, 4)
def test_page_at_the_start(): assert page(list(range(10)), 0) == [0, 1, 2, 3]
