from path import join
from client import url

def test_trailing_slash_not_doubled(): assert join("http://x/", "users") == "http://x/users"
def test_url_with_trailing_slash_base():
    assert url("http://x/", "users", 7) == "http://x/users/7"
def test_plain_join(): assert join("http://x", "y") == "http://x/y"
