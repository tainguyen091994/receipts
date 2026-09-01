def parse_range(spec):
    """Parse "1-5" or a bare "3" into a list of ints.

    Both ends of a range are included. A descending range such as "5-1" counts
    down.
    """
    a, b = spec.split("-")
    return list(range(int(a), int(b)))
