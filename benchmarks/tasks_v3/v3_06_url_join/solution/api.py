from path import join


def endpoint(base, *parts):
    """Build a full endpoint from a base and any number of segments."""
    out = base
    for p in parts:
        out = join(out, p)
    return out
