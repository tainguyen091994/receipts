from config import load

def test_unknown_key_ignored(): assert "extra" not in load({"extra": "1"})
def test_int_coerced(): assert load({"port": "9000"})["port"] == 9000
