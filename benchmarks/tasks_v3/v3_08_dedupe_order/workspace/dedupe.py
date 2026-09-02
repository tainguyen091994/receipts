from keys import norm


def unique(items):
    """Drop duplicates, keeping the FIRST occurrence and its original text."""
    seen, out = set(), []
    for i in items:
        k = norm(i)
        if k not in seen:
            seen.add(k)
            out.append(i)
    return out[::-1]
