def norm(s):
    """Normalise a key for comparison.

    Trimmed and case-folded: two keys differing only in surrounding space or in
    capitalisation are the same key.
    """
    return s.strip().casefold()
