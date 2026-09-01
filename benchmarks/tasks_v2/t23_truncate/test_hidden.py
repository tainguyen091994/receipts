from src import truncate
def test_never_cuts_a_word():
    assert truncate("hello wonderful world", 14) == "hello..."
def test_cut_on_a_space_keeps_the_word():
    assert truncate("hello wonderful world", 16) == "hello..."
def test_exactly_at_limit(): assert truncate("abcdefgh", 8) == "abcdefgh"
