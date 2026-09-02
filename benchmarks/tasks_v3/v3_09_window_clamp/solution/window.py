from clamp import clamp


def visible_range(cursor, size, total):
    """Half-open [start, end) window of `size` items centred on cursor."""
    start = cursor - size // 2
    lo = clamp(start, 0, total - size)
    return (lo, lo + size)
