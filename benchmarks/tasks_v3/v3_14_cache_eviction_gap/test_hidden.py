from index import search, serve
from store import evict, get, put


def test_first_search_serves_the_row():
    put("a", 1, {"text": "bravo"})
    assert serve("a", "bravo") == [{"text": "bravo"}]


def test_get_after_evict_misses():
    put("b", 1, {"text": "hotel"})
    evict("b")
    assert get("b") is None


def test_repeat_search_after_evict_is_empty():
    put("c", 1, {"text": "charlie"})
    serve("c", "charlie")
    evict("c")
    assert serve("c", "charlie") == []


def test_direct_repeat_search_after_evict_is_empty():
    put("d", 1, {"text": "delta"})
    search([get("d")], "delta")
    evict("d")
    assert search([get("d")], "delta") == []


def test_evict_twice_does_nothing():
    put("e", 1, {"text": "juliet"})
    evict("e")
    evict("e")
    assert get("e") is None


def test_repeat_search_after_put_over_shows_no_old_row():
    put("f", 1, {"text": "foxtrot"})
    serve("f", "foxtrot")
    put("f", 2, {"text": "echo"})
    assert serve("f", "foxtrot") == []
