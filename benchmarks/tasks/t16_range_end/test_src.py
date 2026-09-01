from src import countdown
def test_a(): assert countdown(5) == [1,2,3,4,5]
def test_b(): assert countdown(1) == [1]
