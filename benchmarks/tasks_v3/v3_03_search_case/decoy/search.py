from indexer import build
from lexer import tokens


def search(docs, query):
    """Doc ids containing EVERY token of the query."""
    idx = build(docs)
    hits = [set(idx.get(t.lower(), [])) for t in tokens(query)]
    return sorted(set.intersection(*hits)) if hits else []
