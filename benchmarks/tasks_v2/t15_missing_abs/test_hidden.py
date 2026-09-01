from src import distance
def test_b(): assert distance(10, 3) == 7
def test_negatives(): assert distance(-5, -2) == 3
def test_same(): assert distance(4, 4) == 0
