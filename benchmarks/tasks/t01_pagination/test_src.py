from src import page_items
def test_first_page(): assert page_items([1,2,3,4,5,6,7], 1) == [1,2,3]
def test_second_page(): assert page_items([1,2,3,4,5,6,7], 2) == [4,5,6]
def test_last_partial(): assert page_items([1,2,3,4,5,6,7], 3) == [7]
