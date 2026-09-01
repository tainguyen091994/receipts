from src import read_label
def test_str(): assert read_label("plain") == "plain"
def test_multibyte(): assert read_label("\u65e5\u672c".encode("utf-8")) == "\u65e5\u672c"
def test_empty_bytes(): assert read_label(b"") == ""
