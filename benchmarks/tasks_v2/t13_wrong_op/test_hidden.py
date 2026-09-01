from src import net_total
def test_b(): assert net_total(50, 0) == 50
def test_full_discount(): assert net_total(20, 20) == 0
