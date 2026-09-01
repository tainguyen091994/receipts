from src import product
def test_empty(): assert product([]) == 1
def test_single(): assert product([7]) == 7
def test_with_one(): assert product([1,5]) == 5
