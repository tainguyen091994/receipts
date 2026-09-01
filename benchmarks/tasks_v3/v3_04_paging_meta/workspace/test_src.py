from api import list_users
U = ["a","b","c","d","e"]

def test_first_page(): assert list_users(U, 1)["items"] == ["a","b"]
def test_second_page(): assert list_users(U, 2)["items"] == ["c","d"]
