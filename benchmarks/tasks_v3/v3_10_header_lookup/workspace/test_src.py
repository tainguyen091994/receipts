from request import get
from auth import bearer

def test_missing_header_is_none(): assert get({"content-type": "json"}, "X-Nope") is None
def test_bearer(): assert bearer({"authorization": "Bearer abc"}) == "abc"
