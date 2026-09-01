from src import read_label
def test_ascii(): assert read_label(b"hello") == "hello"
def test_utf8(): assert read_label("caf\u00e9".encode("utf-8")) == "caf\u00e9"
