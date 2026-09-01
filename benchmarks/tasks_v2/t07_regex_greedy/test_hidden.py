from src import extract_tags
def test_one(): assert extract_tags("x [only] y") == ["only"]
def test_empty_tag(): assert extract_tags("[] [b]") == ["","b"]
def test_three(): assert extract_tags("[a][b][c]") == ["a","b","c"]
