from headers import canonical
from request import get

def test_underscores_are_hyphens(): assert canonical("Content_Type") == "content-type"
def test_cgi_style_lookup(): assert get({"x-api-key": "k"}, "X_API_KEY") == "k"
def test_plain_canonical(): assert canonical("Accept") == "accept"
