from index import search
from search import handle
from store import get, put


def test_search_finds_row():
    put("k", 1, {"text": "alpha beta"})
    assert search([get("k")], "alpha") == [{"text": "alpha beta"}]


def test_search_misses_when_no_match():
    put("k", 1, {"text": "alpha beta"})
    assert search([get("k")], "gamma") == []


def test_repeat_search_after_evict_is_empty():
    handle(("put", "k", 1, "alpha"))
    handle(("search", "k", "alpha"))
    handle(("evict", "k"))
    assert handle(("search", "k", "alpha")) == []
