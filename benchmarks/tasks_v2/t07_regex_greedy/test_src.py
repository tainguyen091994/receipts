from src import extract_tags
def test_two(): assert extract_tags("[a] and [b]") == ["a","b"]
def test_none(): assert extract_tags("nothing here") == []
