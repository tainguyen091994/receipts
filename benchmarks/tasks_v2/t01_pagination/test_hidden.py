from src import page_items
def test_second_page(): assert page_items([1,2,3,4,5,6,7], 2) == [4,5,6]
def test_custom_per_page(): assert page_items(list(range(1,11)), 2, per_page=4) == [5,6,7,8]
def test_past_end(): assert page_items([1,2,3], 9) == []
