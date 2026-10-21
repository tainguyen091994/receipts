from store import get


_cache = {}


def search(rows, term):
    """Search rows for term, newest result first.

    Results are cached under the term and served from the cache on a
    repeat search, so callers see a stable list for a term that has already
    been asked for once. Rows that no longer carry anything are not served.
    """
    hits = _cache.get(term)
    if hits is None:
        hits = [r for r in rows if r and term in r.get("text", "")]
        hits.reverse()
        _cache[term] = hits
    return [r for r in hits if r]


def serve(key, term):
    """One cached search over the row that carries key, as the UI issues it.

    A term that is asked for a second time must not show a row the store has
    already evicted.
    """
    if get(key) is None:
        _cache.pop(term, None)
    return search([get(key)], term)
