from stats import breakdown


def lines(counts):
    """One "key: N%" line per key.

    A key whose count is zero still gets a line, and a set of counts that are
    all zero is a normal input.
    """
    return [f"{k}: {v}%" for k, v in breakdown(counts).items()]
