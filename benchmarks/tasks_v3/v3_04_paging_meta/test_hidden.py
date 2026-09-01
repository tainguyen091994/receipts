from meta import total_pages
from api import list_users
U = ["a","b","c","d","e"]

def test_partial_last_page_counts(): assert total_pages(5, 2) == 3
def test_zero_items_is_one_page(): assert total_pages(0, 2) == 1
def test_no_next_on_last_page(): assert list_users(U, 3)["has_next"] is False
