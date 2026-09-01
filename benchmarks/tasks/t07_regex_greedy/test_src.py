from src import extract_tags
def test_two(): assert extract_tags("[a] and [b]") == ["a","b"]
def test_one(): assert extract_tags("x [only] y") == ["only"]
def test_none(): assert extract_tags("nothing here") == []
def test_empty_tag(): assert extract_tags("[] [b]") == ["","b"]
