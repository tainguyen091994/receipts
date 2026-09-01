from src import truncate
def test_short_unchanged(): assert truncate("hello", 10) == "hello"
def test_limit_includes_ellipsis(): assert len(truncate("abcdefghij", 8)) <= 8
