from lexer import tokens


def build(docs):
    """token -> sorted list of doc ids."""
    idx = {}
    for i, d in enumerate(docs):
        for t in tokens(d):
            idx.setdefault(t, [])
            if i not in idx[t]:
                idx[t].append(i)
    return {k: sorted(v) for k, v in idx.items()}
