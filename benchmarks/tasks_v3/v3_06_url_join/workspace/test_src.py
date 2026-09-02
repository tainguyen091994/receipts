from client import url

def test_all_segments(): assert url("http://x", "users", 7) == "http://x/users/7"
def test_other_resource(): assert url("http://x", "ping", 1) == "http://x/ping/1"
